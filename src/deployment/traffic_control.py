from gpiozero import LED
from time import sleep

# --- KONFIGURASI PIN LAMPU LALU LINTAS ---
# Format: (Merah, Kuning, Hijau) untuk tiap arah

# Jalur A (Utara) - GPIO 22, 27, 17
red_A = LED(22)
yellow_A = LED(27)
green_A = LED(17)

# Jalur B (Timur) - GPIO 23, 24, 8
red_B = LED(23)
yellow_B = LED(24)
green_B = LED(8)

# Jalur C (Barat) - GPIO 21, 20, 16
red_D = LED(21)
yellow_D = LED(20)
green_D = LED(16)

# Jalur D (Selatan) - GPIO 26, 6, 5
red_C = LED(26)
yellow_C = LED(6)
green_C = LED(5)

# List kelompok lampu berdasarkan jalur (A–D = indeks 0–3)
traffic_lights = [
    (red_A, yellow_A, green_A),  # 0 = Utara (A)
    (red_B, yellow_B, green_B),  # 1 = Timur (B)
    (red_C, yellow_C, green_C),  # 2 = Barat (C)
    (red_D, yellow_D, green_D)   # 3 = Selatan (D)
]

# --- FUNGSI DASAR KONTROL LAMPU ---
def turn_off_all():
    """Matikan semua lampu di semua jalur"""
    for r, y, g in traffic_lights:
        r.off()
        y.off()
        g.off()
    print("[INFO] Semua lampu dimatikan.")

def set_green(index):
    """Nyalakan hijau untuk jalur index tertentu, sisanya merah"""
    turn_off_all()
    for i, (r, y, g) in enumerate(traffic_lights):
        if i == index:
            g.on()
        else:
            r.on()

def set_yellow(index):
    """Nyalakan lampu kuning pada jalur index tertentu"""
    turn_off_all()
    traffic_lights[index][1].on()

# --- FUNGSI SIKLUS OTOMATIS ---
def cycle_traffic():
    """
    Jalankan siklus otomatis lalu lintas: hijau -> kuning -> merah.
    Pause dapat dikendalikan melalui pause_cycle dari globals.py.
    """
    from globals import pause_cycle
    while True:
        for i in range(len(traffic_lights)):
            if pause_cycle.is_set():
                break
            print(f"?? Menyalakan lampu hijau untuk jalur {chr(65+i)}")
            set_green(i)
            sleep(5)