# 🚨 Emergency Vehicle Detection - Deployment Guide

## Overview

Sistem deteksi kendaraan darurat (ambulans, pemadam kebakaran, polisi) menggunakan YOLOv5 yang secara otomatis mengontrol lampu lalu lintas untuk memberikan prioritas jalur.

**Fitur:**
- Real-time detection dengan YOLOv5
- Deteksi audio 4 arah dengan mikrofon USB
- Verifikasi ganda (audio + visual)
- Kontrol servo untuk arahkan kamera
- Kontrol otomatis 4 lampu lalu lintas via GPIO

---

## Hardware Requirements

| Component | Specification |
|-----------|--------------|
| **Board** | Raspberry Pi 5 (4GB/8GB RAM) |
| **Camera** | Picamera2 compatible (Camera Module V2/V3) |
| **Microphones** | 4x USB microphone (North, East, West, South) |
| **Servo** | Standard servo 0-180° (GPIO 12) |
| **Traffic Lights** | 12x LED + resistors (3 per arah) |
| **Power** | 5V 5A for RPi + External 5V 2A for servo |

### GPIO Pin Mapping

| Direction | Red | Yellow | Green | Lane Index |
|-----------|-----|--------|-------|------------|
| North | 22 | 27 | 17 | 0 |
| East | 23 | 24 | 8 | 1 |
| West | 21 | 20 | 16 | 2 |
| South | 26 | 6 | 5 | 3 |

**Servo:** GPIO 12  
**Microphone Order:** USB 1-4 → South, North, West, East

---

## Quick Installation

### Automatic (Recommended)

```bash
cd ~
git clone https://github.com/hadysadya/final-project.git
cd final-project
chmod +x deployment/setup_rpi.sh
./deployment/setup_rpi.sh
```

Script akan install semua dependencies (~15-20 menit).

### Manual Installation

```bash
# 1. System dependencies
sudo apt update && sudo apt upgrade -y
sudo apt install -y python3-pip python3-venv python3-dev \
    libportaudio2 portaudio19-dev libatlas-base-dev \
    libopenblas-dev python3-picamera2

# 2. Create virtual environment
cd ~/final-project
python3 -m venv venv
source venv/bin/activate

# 3. Install Python packages
pip install --upgrade pip
pip install -r deployment/requirements_rpi.txt

# 4. Setup permissions
sudo usermod -a -G gpio,audio,video $USER
```

**Reboot** setelah instalasi untuk apply permissions.

---

## Configuration

### 1. Place Model File

```bash
cp /path/to/model3.torchscript ~/final-project/models/
```

### 2. Verify Microphone Indices

```bash
python3 -c "import pyaudio; p = pyaudio.PyAudio(); \
[print(f'{i}: {p.get_device_info_by_index(i)[\"name\"]}') \
for i in range(p.get_device_count())]; p.terminate()"
```

Update `DEVICE_INDICES` di `src/deployment/config.py` jika perlu.

### 3. Enable Camera

```bash
sudo raspi-config
# Interface Options → Camera → Enable
```

### 4. Adjust Settings (Optional)

Edit `src/deployment/config.py`:

```python
TIMING_CONFIG = {
    'EMERGENCY_HOLD_DURATION': 15,    # Green light duration (sec)
    'AUDIO_COOLDOWN_DURATION': 15,    # Cooldown after emergency (sec)
}

AUDIO_CONFIG = {
    'VOLUME_THRESHOLD_DBFS': -40,     # Audio detection threshold
}

YOLOV5_CONFIG = {
    'CONF_THRESHOLD': 0.25,           # YOLO confidence threshold
}
```

---

## Running the System

### Manual Start

```bash
cd ~/final-project
source venv/bin/activate
python3 src/deployment/main.py
```

### Background Mode

```bash
nohup python3 src/deployment/main.py > logs/system.log 2>&1 &
```

### Auto-start on Boot

```bash
# Create service file
sudo nano /etc/systemd/system/traffic-control.service
```

Paste:

```ini
[Unit]
Description=Emergency Vehicle Detection System
After=network.target

[Service]
Type=simple
User=pi
WorkingDirectory=/home/pi/final-project
Environment="PATH=/home/pi/final-project/venv/bin"
ExecStart=/home/pi/final-project/venv/bin/python3 src/deployment/main.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Enable service:

```bash
sudo systemctl daemon-reload
sudo systemctl enable traffic-control.service
sudo systemctl start traffic-control.service
```

Check status:

```bash
sudo systemctl status traffic-control.service
sudo journalctl -u traffic-control.service -f
```

---

## Troubleshooting

### Camera Not Working

```bash
# Check camera
libcamera-hello --list-cameras

# Test capture
libcamera-still -o test.jpg
```

### Microphones Not Detected

```bash
# List audio devices
arecord -l

# Test recording
arecord -D hw:1,0 -d 5 test.wav
aplay test.wav
```

### GPIO Permission Denied

```bash
# Add user to gpio group
sudo usermod -a -G gpio $USER
sudo reboot
```

### Servo Not Moving

- Check power supply (use **external 5V** for servo)
- Verify GPIO 12 connection
- Test servo:

```python
from gpiozero import AngularServo
servo = AngularServo(12, min_angle=0, max_angle=180)
servo.angle = 90
```

### High CPU Usage

Edit `config.py`:

```python
CAMERA_CONFIG['PREVIEW_SIZE'] = (640, 640)  # Reduce resolution
TIMING_CONFIG['YOLO_DETECTION_INTERVAL'] = 2  # Slower inference
```

### False Positive Detections

```python
YOLOV5_CONFIG['CONF_THRESHOLD'] = 0.35  # Higher confidence
AUDIO_CONFIG['VOLUME_THRESHOLD_DBFS'] = -35  # Less sensitive
```

---

## System Architecture

```
Camera (Picamera2) → YOLO Detection → Label Queue
                                           ↓
4x Microphones → Audio Processing → Main Controller
                                           ↓
                            ┌──────────────┼──────────────┐
                            ↓              ↓              ↓
                        Servo          Traffic        Logging
                       Control         Lights         System
```

**Detection Logic:**
1. Audio detects sound from any direction
2. Servo turns camera to sound source
3. YOLO verifies emergency vehicle visually
4. If verified (audio + visual) → activate green light
5. Hold green for 15 seconds
6. Enter cooldown for 15 seconds

**Special Case:** North direction (camera can't reach) → audio-only trigger

---

## Performance Metrics

| Metric | Value (RPi 5) |
|--------|---------------|
| YOLO Inference | ~200-300ms |
| Audio Latency | <100ms |
| Response Time | <2 seconds |
| CPU Usage | 40-60% |
| RAM Usage | 1.5-2GB |

---

## Maintenance

**Daily:**
- Check system logs: `tail -f logs/system.log`
- Verify 4 microphones working
- Test camera feed

**Weekly:**
- Review detection accuracy
- Check disk space
- Clean old logs: `find logs/ -name "*.log" -mtime +30 -delete`

**Monthly:**
- Update packages: `pip install --upgrade -r deployment/requirements_rpi.txt`
- Backup config: `tar -czf backup.tar.gz src/deployment/config.py models/`

---

## Support

- **Repository:** [github.com/hadysadya/final-project](https://github.com/hadysadya/final-project)
- **Issues:** [GitHub Issues](https://github.com/hadysadya/final-project/issues)

---

**Version:** 1.0.0  
**Last Updated:** December 2024