# 🚨 Emergency Vehicle Detection - Deployment Guide

## Overview

Emergency vehicle detection system (ambulance, fire truck, police) using YOLOv5 which automatically controls traffic lights to give lane priority.

**Feature:**
- Real-time detection with YOLOv5
- 4-way audio detection with USB microphone
- Double verification (audio + visual)
- Servo control to direct the camera
- Automatic control of 4 traffic lights via GPIO

## Hardware Requirements

| Component | Specification |
|-----------|--------------|
| **Board** | Raspberry Pi 5 (8GB RAM) |
| **Camera** | Picamera2 compatible (Camera Module) |
| **Microphones** | 4x USB microphone (North, East, West, South) |
| **Servo** | Standard servo 0-180° (GPIO 12) |
| **Traffic Lights** | 12x LED (3 per direction) |
| **Power** | 5V 5A for RPi + External 2x 3.7V batteries for servo |

### GPIO Pin Mapping

| Direction | Red | Yellow | Green | Lane Index |
|-----------|-----|--------|-------|------------|
| North | 22 | 27 | 17 | 0 |
| East | 23 | 24 | 8 | 1 |
| West | 21 | 20 | 16 | 2 |
| South | 26 | 6 | 5 | 3 |

**Servo:** GPIO 12  
**Microphone Order:** USB 1-4 → South, North, West, East

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

## Performance Metrics

| Metric | Value (RPi 5) |
|--------|---------------|
| YOLO Inference | ~200-300ms |
| Audio Latency | <100ms |
| Response Time | <2 seconds |
| CPU Usage | 40-60% |
| RAM Usage | 1.5-2GB |

## Support

- **Repository:** [github.com/hadysadya/final-project](https://github.com/hadysadya/final-project)
- **Issues:** [GitHub Issues](https://github.com/hadysadya/final-project/issues)

---

**Version:** 1.0.0  
**Last Updated:** July 2025
