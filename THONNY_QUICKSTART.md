# 🎨 Quick Start Guide - Thonny IDE

Complete guide for setting up and running the emergency vehicle detection system.

## 📋 What This System Does

Detects emergency vehicles (ambulance, fire truck, police) using:
- **Audio detection** from 4 microphones (North, South, East, West)
- **Visual verification** with YOLOv5 camera detection
- **Automatic traffic control** via GPIO-controlled LEDs

**Detection logic:**
1. Microphones detect siren sound
2. Camera servo turns toward sound
3. YOLO confirms it's an emergency vehicle
4. If both audio + visual confirmed → green light for 15 seconds

## 📋 Prerequisites

**Hardware Required:**
- Raspberry Pi 5 with all components connected (see [`HARDWARE_SETUP.md`](HARDWARE_SETUP.md) for wiring)
- Components: 4× USB mics, Pi Camera, Servo motor, 12× LEDs

**Software Required:**
- Raspberry Pi OS (64-bit recommended)
- Python 3.11+
- Virtual environment with dependencies installed
- RealVNC Connect enabled

**If not installed yet:**
```bash
# Install system dependencies
sudo apt-get update
sudo apt-get install -y portaudio19-dev python3-pyaudio

# Clone repository
cd ~
git clone https://github.com/hadysadya/final-project.git
cd final-project

# Create virtual environment
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Enable camera interface
sudo raspi-config  # Interface Options → Camera → Enable
```

## ⚙️ One-Time Setup

### 1. Access Raspberry Pi via RealVNC

**RealVNC Connection:**
- Address: `<your-pi-ip>`  *(Find with `hostname -I` on Pi)*
- Username: `<your-username>`
- Password: `<your-password>`

**Security:** Change default password: `passwd`

### 2. Configure Thonny IDE

**Open Thonny:** Applications Menu → Programming → Thonny Python IDE

**Set Python Interpreter:**
1. Tools → Options → Interpreter tab
2. Select: "Alternative Python 3 interpreter"
3. Browse to: `/home/<username>/final-project/venv/bin/python3`
4. Click OK
5. Verify bottom-right shows: `Python 3.11.x`

**Set Working Directory:**
1. View → Files (to open file browser)
2. Navigate to: `/home/<username>/final-project`
3. Right-click folder → "Set as working directory"

**Configure Shell:**
1. Tools → Options → Shell tab
2. Enable: "Execute in separate process"
3. Click OK

## ▶️ Running the System

### Method 1: Via Thonny (Recommended for Development)

1. **Open main file:**
   - File → Open
   - Navigate to: `src/deployment/main.py`

2. **Run:**
   - Click **▶️ Run** button (or press **F5**)

3. **Expected output:**
```
   Microphone 0 initialized successfully.
   Microphone 1 initialized successfully.
   Microphone 2 initialized successfully.
   Microphone 3 initialized successfully.
   Servo initialized successfully.
   Starting object detection...
   Real-time audio volume-based decision started...
```

4. **Stop:**
   - Click **🛑 Stop** button (or press **Ctrl+C**)

### Method 2: Via Terminal (For Long Sessions)
```bash
cd ~/final-project
source venv/bin/activate
python3 src/deployment/main.py
```

**Stop:** Press **Ctrl+C**

## ⌨️ Thonny Shortcuts

| Action | Shortcut |
|--------|----------|
| Run program | F5 |
| Stop program | Ctrl+C |
| Comment lines | Ctrl+3 |
| Uncomment lines | Ctrl+Shift+3 |
| Find text | Ctrl+F |
| Auto-complete | Ctrl+Space |

## 🔧 Troubleshooting

### "No module named 'torch'"
**Cause:** Virtual environment not activated in Thonny  
**Fix:** Recheck interpreter setting (Setup step 2)

### "Permission denied: /dev/gpiomem"
**Fix:**
```bash
sudo usermod -a -G gpio $USER
sudo reboot
```

### "Microphone not initialized"
**Fix:**
```bash
# Check USB devices
lsusb

# List audio devices
arecord -l

# Try different USB ports
```

### Camera not working
**Fix:**
```bash
# Test camera
libcamera-hello

# Enable interface
sudo raspi-config  # Interface Options → Camera
```

### GPIO conflicts (pins already in use)
**Fix:** Stop program completely before re-running. If persistent: `sudo reboot`

## 🔄 Typical Workflows

### Daily Development
1. Connect via RealVNC
2. Open Thonny → `main.py` (auto-opens from last session)
3. Run (F5) → Test hardware → Monitor output
4. Make code changes
5. Stop (Ctrl+C) → Re-run to test
6. Repeat

### Demo/Presentation
1. Connect via RealVNC
2. Open Thonny
3. Run program
4. Demonstrate live detection (trigger with siren sound or emergency vehicle)
5. Show traffic light response
6. Stop when done

## 📚 Additional Documentation

- **Hardware specs & wiring:** [`HARDWARE_SETUP.md`](HARDWARE_SETUP.md)
- **Dataset information:** [`dataset/README_DATASET.md`](dataset/README_DATASET.md)
- **Training your own model:** [`notebooks/training_notebook.ipynb`](notebooks/training_notebook.ipynb)

---

**Note:** Thonny remembers your last opened files, working directory, and interpreter settings between sessions.
