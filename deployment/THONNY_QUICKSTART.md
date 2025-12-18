# 🎨 Quick Start Guide - Thonny IDE Workflow

## 📌 Overview

Panduan ini khusus untuk menjalankan Emergency Vehicle Detection System menggunakan Thonny IDE di Raspberry Pi 5 yang diakses via RealVNC Viewer.

---

## 🖥️ Setup Environment

### 1. Akses Raspberry Pi via RealVNC

```
Laptop → RealVNC Viewer → Raspberry Pi 5 Desktop
```

**RealVNC Connection:**
- Address: `192.168.x.x` (IP Raspberry Pi Anda)
- Username: `admin`
- Password: `[your-password]`

### 2. Buka Thonny IDE

**Location:** Applications Menu → Programming → Thonny Python IDE

---

## ⚙️ Konfigurasi Thonny (One-time Setup)

### Step 1: Set Python Interpreter

1. **Tools → Options**
2. Tab **"Interpreter"**
3. Pilih: **"Alternative Python 3 interpreter"**
4. Browse ke: `/home/admin/TAedward/yolo_object/bin/python3`
5. Click **OK**

**Verify:**
- Lihat di bottom-right Thonny: Should show `Python 3.11.2`

### Step 2: Set Working Directory

1. **View → Files** (untuk buka file browser)
2. Navigate ke: `/home/admin/TAedward/final-project`
3. Right-click folder → **"Set as working directory"**

### Step 3: Configure Shell

1. **Tools → Options**
2. Tab **"Shell"**
3. ✅ Enable: "Execute in separate process"
4. Click **OK**

---

## 📁 Project Structure dalam Thonny

```
📂 /home/admin/TAedward/final-project/
├── 📂 src/
│   └── 📂 deployment/
│       ├── 📄 __init__.py
│       ├── 📄 config.py          ← Edit konfigurasi di sini
│       ├── 📄 main.py            ← ▶️ RUN FILE INI
│       ├── 📄 detect_yolov5.py
│       ├── 📄 traffic_control.py
│       └── 📄 globals.py
├── 📂 models/
│   ├── 📂 [yolov5 models folder]
│   └── 📄 model3.torchscript     ← Model file (7MB)
├── 📂 utils/
│   └── 📂 [yolov5 utils folder]
└── 📂 logs/
    └── 📄 system.log
```

---

## ▶️ Cara Menjalankan Program

### Method 1: Run via Thonny (Recommended)

1. **Open Main File:**
   - File → Open
   - Navigate: `src/deployment/main.py`

2. **Check Configuration** (optional):
   - File → Open → `src/deployment/config.py`
   - Review settings (audio threshold, timing, dll)
   - Save if modified

3. **Run Program:**
   - Click tombol **▶️ Run** (atau tekan **F5**)
   - Atau: Run → Run current script

4. **Monitor Output:**
   - Output akan muncul di **Shell** (bottom panel)
   - Watch for:
     ```
     Microphone 0 initialized successfully.
     Microphone 1 initialized successfully.
     Microphone 2 initialized successfully.
     Microphone 3 initialized successfully.
     Servo initialized successfully.
     [INFO] Object detection started.
     Real-time audio volume-based decision started...
     ```

### Method 2: Run via Terminal (Alternative)

Jika prefer terminal:

1. **Open Terminal** di Raspberry Pi Desktop
2. **Navigate & Activate venv:**
   ```bash
   cd /home/admin/TAedward/final-project
   source ../yolo_object/bin/activate
   ```
3. **Run:**
   ```bash
   python3 src/deployment/main.py
   ```

---

## 🛑 Cara Menghentikan Program

### Stop via Thonny:
- Click tombol **🛑 Stop** (atau tekan **Ctrl+C**)
- Atau: Run → Interrupt execution

### Stop via Terminal:
- Press **Ctrl+C**

**Note:** Program akan cleanup threads dengan graceful shutdown.

---

## 🔧 Edit Configuration

### Adjust Settings via Thonny

1. **Open config.py:**
   ```
   File → Open → src/deployment/config.py
   ```

2. **Common Adjustments:**

**Adjust Emergency Duration:**
```python
TIMING_CONFIG = {
    'EMERGENCY_HOLD_DURATION': 15,  # Change to 10, 20, etc.
}
```

**Adjust Audio Sensitivity:**
```python
AUDIO_CONFIG = {
    'VOLUME_THRESHOLD_DBFS': -40,  # -30 = less sensitive, -50 = more sensitive
}
```

**Adjust YOLO Confidence:**
```python
YOLOV5_CONFIG = {
    'CONF_THRESHOLD': 0.25,  # 0.30 = stricter, 0.20 = looser
}
```

**Change Camera Resolution:**
```python
CAMERA_CONFIG = {
    'PREVIEW_SIZE': (640, 640),  # Lower for better performance
}
```

3. **Save:** File → Save (or Ctrl+S)

4. **Re-run program** untuk apply changes

---

## 🧪 Testing Individual Components

### Test 1: Check Microphones

**Create new file:** `test_microphones.py`

```python
import pyaudio

p = pyaudio.PyAudio()
print(f"Total audio devices: {p.get_device_count()}\n")

for i in range(p.get_device_count()):
    info = p.get_device_info_by_index(i)
    print(f"Device {i}:")
    print(f"  Name: {info['name']}")
    print(f"  Input channels: {info['maxInputChannels']}")
    print(f"  Output channels: {info['maxOutputChannels']}")
    print()

p.terminate()
```

**Run:** Click ▶️ Run

**Expected Output:**
```
Total audio devices: 8

Device 0:
  Name: USB Microphone 1
  Input channels: 1
  ...
```

### Test 2: Check Camera

**Create new file:** `test_camera.py`

```python
from picamera2 import Picamera2
import time

picam = Picamera2()
config = picam.create_still_configuration()
picam.configure(config)
picam.start()

print("Camera started. Taking picture in 2 seconds...")
time.sleep(2)

picam.capture_file("test_image.jpg")
print("Image saved as test_image.jpg")

picam.stop()
```

**Run:** Click ▶️ Run

### Test 3: Check GPIO & Servo

**Create new file:** `test_servo.py`

```python
from gpiozero import AngularServo
import time

servo = AngularServo(12, min_angle=0, max_angle=180)

print("Testing servo movement...")
angles = [0, 45, 90, 135, 180, 90]

for angle in angles:
    print(f"Moving to {angle}°")
    servo.angle = angle
    time.sleep(1)

print("Servo test complete!")
```

**Run:** Click ▶️ Run

### Test 4: Check Traffic Lights

**Create new file:** `test_traffic_lights.py`

```python
from gpiozero import LED
import time

# Test North lane (GPIO 22, 27, 17)
red = LED(22)
yellow = LED(27)
green = LED(17)

print("Testing North lane traffic lights...")

print("Red ON")
red.on()
time.sleep(2)
red.off()

print("Yellow ON")
yellow.on()
time.sleep(2)
yellow.off()

print("Green ON")
green.on()
time.sleep(2)
green.off()

print("Test complete!")
```

**Run:** Click ▶️ Run

---

## 📊 Monitor System Performance

### Check CPU & RAM Usage

**Create file:** `monitor_performance.py`

```python
import psutil
import time

while True:
    cpu_percent = psutil.cpu_percent(interval=1)
    ram = psutil.virtual_memory()
    ram_used_gb = ram.used / (1024**3)
    ram_total_gb = ram.total / (1024**3)
    ram_percent = ram.percent
    
    print(f"CPU: {cpu_percent}% | RAM: {ram_used_gb:.2f}/{ram_total_gb:.2f}GB ({ram_percent}%)")
    time.sleep(2)
```

**Run while main program is running** to monitor resources.

---

## 🐛 Debug Mode

### Enable Verbose Output

Edit `main.py`, add at top:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Add Debug Prints

In your code, add:

```python
print(f"[DEBUG] Variable value: {variable}")
print(f"[DEBUG] Function called with: {param}")
```

### Use Thonny Debugger

1. Set breakpoints: Click on line number
2. Run in Debug mode: Click **🐞 Debug** (or Ctrl+F5)
3. Use controls:
   - **Step over** (F6)
   - **Step into** (F7)
   - **Step out** (F8)
   - **Resume** (F5)

---

## 💡 Tips & Tricks

### Tip 1: Multiple Files Open

- Use **tabs** at top to switch between files
- File → Open recent → Quick access to recent files

### Tip 2: Split View

- View → Split view → Edit two files side-by-side
- Useful for editing `config.py` while viewing `main.py`

### Tip 3: Quick Comment/Uncomment

- Select lines
- **Ctrl+3** to comment
- **Ctrl+Shift+3** to uncomment

### Tip 4: Find & Replace

- **Ctrl+F** to find
- **Ctrl+H** to replace

### Tip 5: Auto-Complete

- Start typing → Press **Ctrl+Space** for suggestions

### Tip 6: Save Session

Thonny remembers:
- Last opened files
- Working directory
- Interpreter settings

So next time you open Thonny, just click Run!

---

## 🔄 Typical Workflow

### Daily Development Cycle:

1. **Connect via RealVNC** to Raspberry Pi
2. **Open Thonny IDE**
3. **Open `main.py`** (usually auto-opens from last session)
4. **Review/Edit `config.py`** if needed
5. **Run program** (F5)
6. **Test hardware** (mic, camera, servo, lights)
7. **Monitor output** in Shell
8. **Make adjustments** if needed
9. **Re-run** to test changes
10. **Stop program** (Ctrl+C) when done

### Demo/Presentation:

1. **Connect RealVNC**
2. **Open Thonny**
3. **Open `main.py`**
4. **Click Run ▶️**
5. **Show live detection** on screen
6. **Trigger emergency** (test with audio/vehicle)
7. **Observe traffic light control**
8. **Stop when demo complete**

---

## 📝 Notes

- **VNC Lag:** If video preview lags, consider disabling CV2 window:
  ```python
  # In config.py
  CAMERA_CONFIG['SHOW_DETECTION_WINDOW'] = False
  ```

- **Long Running:** For extended testing, use Terminal instead of Thonny to avoid IDE overhead

- **Multiple Runs:** Stop program completely before re-running to avoid GPIO conflicts

---

## 🆘 Common Issues

### Issue: "Port already in use"

**Cause:** Previous run didn't cleanup properly

**Solution:**
```bash
# In Terminal
sudo pkill -f main.py
# Or reboot
sudo reboot
```

### Issue: Thonny frozen

**Solution:**
- **Ctrl+C** in Shell
- If still frozen: Close Thonny, reopen
- Worst case: Reboot Raspberry Pi

### Issue: Import errors

**Solution:**
```python
# Add at top of main.py
import sys
sys.path.insert(0, '/home/admin/TAedward/final-project')
```

---

## ✅ Checklist - Ready to Run

Before each run, verify:

- [ ] RealVNC connected
- [ ] Thonny IDE open
- [ ] Virtual environment set correctly
- [ ] Working directory = `/home/admin/TAedward/final-project`
- [ ] 4 microphones connected (USB hub)
- [ ] Camera connected
- [ ] Servo connected (external power!)
- [ ] Traffic light LEDs connected
- [ ] `main.py` opened in Thonny
- [ ] Configuration checked in `config.py`

**Ready? Click Run! ▶️**

---

**Happy Coding! 🚀**