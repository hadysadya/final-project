# 🚨 Emergency Vehicle Detection & Traffic Control System

Real-time emergency vehicle detection using YOLOv5 with automatic traffic light priority control.

[![Python](https://img.shields.io/badge/Python-3.11.2-blue.svg)](https://www.python.org/)
[![YOLOv5](https://img.shields.io/badge/YOLOv5-Deployed-green.svg)](https://github.com/ultralytics/yolov5)
[![Platform](https://img.shields.io/badge/Platform-Raspberry%20Pi%205-red.svg)](https://www.raspberrypi.com/)
[![Status](https://img.shields.io/badge/Status-Prototype-yellow.svg)](https://github.com/hadysadya/final-project)

## 📋 What is This?

Proof-of-concept system that detects emergency vehicles (ambulance, fire truck, police) using **computer vision + audio detection**, then automatically gives them traffic light priority.

**Key Technologies:**
- YOLOv5 for real-time object detection
- 4-microphone array for directional audio
- Dual verification to reduce false positives
- Raspberry Pi 5 with GPIO control

## ⚠️ Prototype Disclaimer

This is an **academic prototype** for educational purposes only.

**Suitable for:**
- ✅ Academic demonstration
- ✅ Technology proof-of-concept
- ✅ Learning embedded AI systems

**NOT suitable for:**
- ❌ Production deployment
- ❌ Real traffic scenarios
- ❌ Safety-critical applications

## 🚀 Quick Start

### For Users

**See:** [`THONNY_QUICKSTART.md`](THONNY_QUICKSTART.md)

Quick summary:
```bash
cd ~/final-project
source venv/bin/activate
python3 src/deployment/main.py
```

### For Hardware Setup

**See:** [`HARDWARE_SETUP.md`](HARDWARE_SETUP.md)

Includes GPIO pin mappings, component specs, and wiring details.

### For Training Your Own Model

**See:** [`notebooks/training_notebook.ipynb`](notebooks/training_notebook.ipynb)

Train on Google Colab with your own dataset.

## 📂 Repository Structure
```
final-project/
├── dataset/                 # Training dataset 
├── exp_results/             # Training result
├── images/                  # Demo documentation
├── models/                  # Trained YOLOv5 model
├── notebooks/               # Training notebook
├── src/deployment/          # Main application code
├── .gitignore               # Ignore file
├── HARDWARE_SETUP.md        # Hardware specifications
├── README.md                # This file
├── THONNY_QUICKSTART.md     # User guide
└── requirements.txt         # Dependencies
```

## 📚 Documentation

| Document | Purpose |
|----------|---------|
| [THONNY_QUICKSTART.md](THONNY_QUICKSTART.md) | Setup and run the system |
| [HARDWARE_SETUP.md](HARDWARE_SETUP.md) | Hardware specs and GPIO mapping |
| [dataset/README_DATASET.md](dataset/README_DATASET.md) | Dataset information |
| [notebooks/training_notebook.ipynb](notebooks/training_notebook.ipynb) | Model training guide |

## 🎓 Academic Context
**Final Project** - Telkom University  
**Course:** Thesis  
**Supervisors:** Yulinda Eliskar & Rita Purnamasari  
**Year:** 2025

**Demonstrates:**
- Computer vision in traffic management
- Multi-modal sensor fusion 
- Real-time embedded systems
- IoT integration

## 📊 Performance
| Metric | Value |
|--------|-------|
| Detection Accuracy | ~87% |
| Response Time | ~35 milliseconds |
| System Uptime | ~2 hours continuous |

## 🛠️ Technology Stack

Python 3.11 • PyTorch • YOLOv5 • OpenCV • PyAudio • Raspberry Pi 5 • GPIO

## 📞 Contact

**Author:** Hady Sadya  
**Email:** hady17306@gmail.com  
**GitHub:** [@hadysadya](https://github.com/hadysadya)

---

**Version:** 1.0.0 | July 2025
