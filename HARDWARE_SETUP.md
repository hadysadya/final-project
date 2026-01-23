# 🔧 Hardware Setup Reference

Hardware specifications and GPIO pin mappings for the emergency vehicle detection system.

**For setup and running instructions:** See [`THONNY_QUICKSTART.md`](THONNY_QUICKSTART.md)

---

## 🔧 Required Components

| Component | Specification |
|-----------|--------------|
| **Board** | Raspberry Pi 5 (4GB+ RAM recommended) |
| **Camera** | Raspberry Pi Camera Module v2/v3 |
| **Microphones** | 4x USB microphones |
| **Servo** | Standard servo 0-180° |
| **LEDs** | 12x LEDs (Red, Yellow, Green × 4 directions) |
| **Power** | 5V 5A for RPi + 2× 3.7V batteries for servo |

---

## 📍 GPIO Pin Mapping

### Traffic Lights

| Direction | Red | Yellow | Green | Lane Index |
|-----------|-----|--------|-------|------------|
| North | 22 | 27 | 17 | 0 |
| East | 23 | 24 | 8 | 1 |
| West | 21 | 20 | 16 | 2 |
| South | 26 | 6 | 5 | 3 |

### Servo Motor

**Pin:** GPIO 12  
**Range:** 0-180°  
**Power:** External batteries (servo draws high current, don't power from Pi)

### Microphone Mapping

| Device Index | Direction | USB Port | Camera Can Reach? |
|--------------|-----------|----------|-------------------|
| 0 | South | 1 | ✅ Yes |
| 1 | North | 2 | ❌ No (blocked) |
| 2 | West | 3 | ✅ Yes |
| 3 | East | 4 | ✅ Yes |

**Note:** North direction uses audio-only detection (camera physically blocked).

---

## 📊 System Architecture
```
┌─────────────┐
│   Camera    │──→ YOLO Detection ──→ Label Queue
└─────────────┘                           │
                                          ↓
┌─────────────┐                     ┌──────────────┐
│ 4× Mics     │──→ Audio Process ──→│ Main Control │
└─────────────┘                     └──────┬───────┘
                                           │
                         ┌─────────────────┼─────────────────┐
                         ↓                 ↓                 ↓
                       Servo            Traffic           Logging
                      Control           Lights            System
```

**Flow:**
1. Audio monitors 4 directions
2. Servo points camera to loudest sound
3. YOLO verifies emergency vehicle
4. Main controller activates traffic light if verified

---

## 📈 Performance Specifications

| Metric | Value (RPi 5) |
|--------|---------------|
| YOLO Inference | ~200-300ms |
| Audio Latency | <100ms |
| Total Response | <2 seconds |
| CPU Usage | 40-60% |
| RAM Usage | 1.5-2GB |

*Estimated values with YOLOv5n model

---

## 📚 Related Documentation

- **Setup & Running:** [`THONNY_QUICKSTART.md`](THONNY_QUICKSTART.md)
- **Dataset Info:** [`dataset/README_DATASET.md`](dataset/README_DATASET.md)
- **Training Guide:** [`notebooks/training_notebook.ipynb`](notebooks/training_notebook.ipynb)

---

Version 1.0.0 | January 2026
