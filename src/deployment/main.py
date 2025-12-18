import pyaudio
import numpy as np
import time
import threading
import lalulintas
from globals import pause_cycle
from detectyolov5 import run
from gpiozero import AngularServo
from queue import Queue

# --- KONSTANTA KONFIGURASI ---
CHUNK = 2048
SAMP_RATE = 44100
PYAUDIO_FORMAT = pyaudio.paInt16
CHANS = 1
MAX_16BIT_VALUE = 32767 # Nilai maksimum untuk audio 16-bit signed

# Sudut Servo
SERVO_ANGLE_WEST = 35
SERVO_ANGLE_SOUTH = 75
SERVO_ANGLE_EAST = 105

# Pengatur Waktu
EMERGENCY_HOLD_DURATION_SECONDS = 15 # Durasi lampu hijau prioritas
AUDIO_RESTART_INTERVAL_SECONDS = 60 # Interval untuk me-restart loop audio
VOLUME_THRESHOLD_DBFS = -40 # Ambang batas suara minimum
AUDIO_COOLDOWN_DURATION_SECONDS = 15 # Durasi cooldown deteksi suara setelah emergency terpicu

# --- FUNGSI AUDIO ---
def pyserial_start(dev_indices):
    """
    Menginisialisasi PyAudio dan membuka stream untuk indeks mikrofon yang ditentukan.
    """
    audio = pyaudio.PyAudio()
    streams = {}
    for dev_index in dev_indices:
        try:
            stream = audio.open(
                format=PYAUDIO_FORMAT,
                rate=SAMP_RATE,
                channels=CHANS,
                input_device_index=dev_index,
                input=True,
                frames_per_buffer=CHUNK
            )
            streams[dev_index] = stream
            print(f'Microphone {dev_index} initialized successfully.')
        except Exception as e:
            print(f'Error initializing microphone {dev_index}: {e}')
    return streams, audio

def pyserial_end(streams, audio):
    """
    Menutup semua stream audio dan menghentikan PyAudio.
    """
    for stream in streams.values():
        if stream.is_active():
            stream.stop_stream()
        stream.close()
    audio.terminate()
    print('Audio streams closed and PyAudio terminated.')

# --- KLASIFIKASI AUDIO DAN KONTROL ---
def classify_audio_volume_based(streams, label_queue, servo, stop_event):
    """
    Membaca audio secara kontinu dari mikrofon, menghitung volume, dan mengontrol
    lalu lintas berdasarkan arah suara terkeras dan deteksi YOLO.
    """
    print('Real-time audio volume-based decision started...')
    
    last_emergency_ts = 0 
    
    # --- Tambahan untuk Cooldown Audio ---
    audio_cooldown_active = False
    audio_cooldown_end_time = 0

    try:
        while not stop_event.is_set():
            # Mengambil label YOLO yang dideteksi SEBELUM memproses audio,
            # agar data visual terbaru selalu tersedia.
            try:
                yolo_label = label_queue.get_nowait() # Coba ambil tanpa menunggu
                print(f"[YOLO] Detected label: {yolo_label}")
            except: 
                yolo_label = None

            volumes_rms = {}
            volumes_db = {}
            
            # --- Bagian 1: Tentukan mikrofon terkeras yang di atas ambang batas suara ---
            # Hanya lakukan deteksi suara jika cooldown tidak aktif
            if not audio_cooldown_active or time.time() >= audio_cooldown_end_time:
                audio_cooldown_active = False # Reset cooldown jika sudah berakhir
                for dev_index, stream in streams.items():
                    try:
                        stream_data = stream.read(CHUNK, exception_on_overflow=False)
                    except Exception as e:
                        print(f"[ERROR] Reading mic {dev_index}: {e}")
                        continue
                    
                    if not stream_data:
                        continue

                    raw_audio = np.frombuffer(stream_data, dtype=np.int16)
                    rms = np.sqrt(np.mean(raw_audio.astype(np.float32) ** 2))
                    volumes_rms[dev_index] = rms
                    
                    if rms > 0:
                        dbfs = 20 * np.log10(rms / MAX_16BIT_VALUE)
                    else:
                        dbfs = -np.inf 
                    volumes_db[dev_index] = dbfs
                    print(f'Microphone {dev_index}: RMS = {rms:.2f}, dBFS = {dbfs:.2f} dB')

                if not volumes_rms:
                    time.sleep(0.1)
                    continue

                loudest_dev = None
                max_dbfs = -np.inf
                for dev_index, dbfs_val in volumes_db.items():
                    if dbfs_val > max_dbfs and dbfs_val >= VOLUME_THRESHOLD_DBFS:
                        max_dbfs = dbfs_val
                        loudest_dev = dev_index
            else:
                # Sedang dalam mode cooldown, lewati deteksi suara baru
                print(f"[INFO] Audio detection is in cooldown mode. Resuming in {int(audio_cooldown_end_time - time.time())}s.")
                loudest_dev = None # Pastikan loudest_dev diset None saat cooldown
                max_dbfs = -np.inf # Pastikan max_dbfs diset ke nilai non-aktif
            
            # --- Bagian 2: SEGERA Arahkan kamera ke arah suara terkeras ---
            # Servo akan berputar hanya jika loudest_dev terdeteksi dan bukan dalam cooldown
            if loudest_dev is not None:
                print(f"[INFO] Loudest direction: Microphone {loudest_dev} (dBFS: {max_dbfs:.2f} dB)")
                
                if loudest_dev == 2: # Barat
                    servo.angle = SERVO_ANGLE_WEST
                    print("Servo turned to West.")
                elif loudest_dev == 1: # Utara (kasus spesial, tidak ada gerakan servo)
                    print("Servo cannot turn to North due to physical limitations.")
                elif loudest_dev == 0: # Selatan
                    servo.angle = SERVO_ANGLE_SOUTH
                    print("Servo turned to South.")
                elif loudest_dev == 3: # Timur
                    servo.angle = SERVO_ANGLE_EAST
                    print("Servo turned to East.")
            else:
                # Jika tidak ada suara signifikan atau sedang cooldown
                print("[INFO] No significant sound detected above threshold or in cooldown.")
            
            # --- Bagian 3: YOLO sudah mengambil label di awal loop, sekarang gunakan hasilnya ---
            emergency_detected = yolo_label in ["Fire Truck", "Ambulance", "Police Car"]

            # --- Bagian 4: Logika Kontrol Lampu Lalu Lintas Berbasis Verifikasi ---
            is_verified_emergency = False

            # KASUS SPESIAL: SUARA TERDETEKSI DARI UTARA
            # Jika suara terkeras datang dari Utara, itu sudah cukup untuk verifikasi
            if loudest_dev == 1 and max_dbfs >= VOLUME_THRESHOLD_DBFS:
                is_verified_emergency = True
                print(f"[ALERT] Emergency detected by sound from North. Prioritizing traffic for North lane.")
                last_emergency_ts = time.time()
                pause_cycle.set()
                lalulintas.set_green(0) # Aktifkan lampu hijau Utara (asumsi 0 = Utara)
                audio_cooldown_active = True # Aktifkan cooldown
                audio_cooldown_end_time = time.time() + AUDIO_COOLDOWN_DURATION_SECONDS
            
            # Untuk arah selain Utara, kita masih butuh verifikasi ganda (suara + visual)
            elif emergency_detected and loudest_dev is not None:
                # Mic yang terjangkau kamera adalah (Selatan), (Barat), (Timur)
                if loudest_dev in [0, 2, 3]: 
                    is_verified_emergency = True
                    print(f"[ALERT] Emergency detected by YOLO AND sound from Mic {loudest_dev}. Prioritizing traffic.")
                    last_emergency_ts = time.time()
                    pause_cycle.set()

                    if loudest_dev == 0: # Jalur Selatan
                        lalulintas.set_green(3) # Asumsi 3 = Selatan
                    elif loudest_dev == 2: # Jalur Barat
                        lalulintas.set_green(2) # Asumsi 2 = Barat
                    elif loudest_dev == 3: # Jalur Timur
                        lalulintas.set_green(1) # Asumsi 1 = Timur
                    
                    audio_cooldown_active = True # Aktifkan cooldown
                    audio_cooldown_end_time = time.time() + AUDIO_COOLDOWN_DURATION_SECONDS
                else:
                    print("[INFO] YOLO detected emergency, but sound direction not suitable for camera verification (or mic not loud enough). Traffic light remains normal.")
                    # Jika sebelumnya mode darurat aktif karena suatu alasan, matikan.
                    if pause_cycle.is_set():
                        pause_cycle.clear()

            # Ini adalah blok untuk kembali ke operasi normal jika tidak ada darurat yang terverifikasi
            if not is_verified_emergency:
                # Logic untuk melepas hold dan mengembalikan ke siklus normal
                if time.time() - last_emergency_ts >= EMERGENCY_HOLD_DURATION_SECONDS:
                    if pause_cycle.is_set():
                        print("[INFO] Emergency hold ended. Resuming traffic cycle.")
                        pause_cycle.clear()
                    print("[INFO] Normal traffic cycle in effect.")
                else:
                    # Masih dalam periode 'emergency hold' (ini berarti ada verifikasi ganda sebelumnya yang masih aktif)
                    print(f"[INFO] Still in emergency hold (remaining: {EMERGENCY_HOLD_DURATION_SECONDS - (time.time() - last_emergency_ts):.1f}s).")

            time.sleep(1)

    except KeyboardInterrupt:
        print("\nAudio detection loop stopped by user.")
    except Exception as e:
        print(f"\n[CRITICAL ERROR] Audio detection crashed: {e}")
    finally:
        for stream in streams.values():
            if stream.is_active():
                stream.stop_stream()
        print('Audio streams stopped.')

# --- FUNGSI DETEKSI OBJEK ---
def run_object_detection(label_queue):
    """
    Memulai proses deteksi objek YOLOv5.
    """
    print("Starting object detection...")
    try:
        run(
            weights='model3.torchscript',
            imgsz=(640, 640),
            conf_thres=0.25,
            iou_thres=0.45,
            device='cpu',
            output_queue=label_queue
        )
    except Exception as e:
        print(f"[CRITICAL ERROR] Object detection crashed: {e}")

# --- LOOP UTAMA UNTUK RESTART AUDIO ---
def restart_audio_loop(dev_indices, label_queue, servo):
    """
    Mengelola siklus hidup thread deteksi audio, me-restart secara berkala.
    """
    while True:
        print(f"\n[INFO] Restarting audio detection in {AUDIO_RESTART_INTERVAL_SECONDS} seconds...")
        stop_event = threading.Event()

        streams, audio = pyserial_start(dev_indices)

        if not streams:
            print("[ERROR] No audio streams could be initialized. Retrying after delay.")
            pyserial_end(streams, audio)
            time.sleep(5) # Jeda sebelum mencoba lagi
            continue

        audio_thread = threading.Thread(
            target=classify_audio_volume_based,
            args=(streams, label_queue, servo, stop_event)
        )
        audio_thread.start()

        time.sleep(AUDIO_RESTART_INTERVAL_SECONDS)

        print("[INFO] Stopping audio detection for restart...")
        stop_event.set()
        audio_thread.join(timeout=10)

        if audio_thread.is_alive():
            print("[WARNING] Audio thread did not terminate gracefully. Forcing cleanup.")
        
        pyserial_end(streams, audio)

# --- BLOK EKSEKUSI UTAMA ---
if __name__ == "__main__":
    label_queue = Queue()
    
    # Inisialisasi servo
    try:
        servo = AngularServo(
            pin=12,
            min_angle=0,
            max_angle=180,
            min_pulse_width=0.0005,
            max_pulse_width=0.0025
        )
        print("Servo initialized successfully.")
    except Exception as e:
        print(f"[ERROR] Could not initialize servo: {e}. Please check wiring and RPi.GPIO setup.")
        exit()

    # Perbaiki pemetaan mikrofon ke arah dan lampu lalu lintas untuk konsistensi
    # Mikrofon:
    # dev_index 0: Selatan (kamera bisa menjangkau)
    # dev_index 1: Utara (kamera TIDAK bisa menjangkau)
    # dev_index 2: Barat (kamera bisa menjangkau)
    # dev_index 3: Timur (kamera bisa menjangkau)
    dev_indices = [0, 1, 2, 3] # Indeks perangkat mikrofon Anda

    try:
        obj_detection_thread = threading.Thread(target=run_object_detection, args=(label_queue,))
        traffic_thread = threading.Thread(target=lalulintas.cycle_traffic)
        
        obj_detection_thread.daemon = True
        traffic_thread.daemon = True
        
        obj_detection_thread.start()
        traffic_thread.start()

        restart_audio_loop(dev_indices, label_queue, servo)

    except KeyboardInterrupt:
        print("\nProgram stopped by user. Cleaning up threads...")
    except Exception as e:
        print(f"\n[CRITICAL ERROR] Main program crashed: {e}")
    finally:
        print("Main program ending.")