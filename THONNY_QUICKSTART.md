# 🎨 Quick Start Guide - Thonny IDE

Simple guide for running the system using Thonny IDE on Raspberry Pi 5 via RealVNC.

## 📋 Prerequisites

**Hardware:** Raspberry Pi 5, 4x USB mics, Pi Camera, Servo, LED traffic lights  
**Software:** Raspberry Pi OS, Python 3.11+, RealVNC Connect, virtual environment installed

## ⚙️ Setup (One-time)

### 1. Access Raspberry Pi

**RealVNC Connection:**
- Address: `<your-pi-ip-address>`  *(Find with `hostname -I` on Pi)*
- Username: `<your-username>`
- Password: `<your-password>`

**Security:** Change default credentials immediately: `passwd`

### 2. Configure Thonny

**Set Interpreter:**
1. Tools → Options → Interpreter tab
2. Select: "Alternative Python 3 interpreter"
3. Browse to: `/home/<username>/final-project/venv/bin/python3`
4. Click OK
5. Verify: Bottom-right shows `Python 3.11.x`

**Set Working Directory:**
1. View → Files
2. Navigate to: `/home/<username>/final-project`
3. Right-click → "Set as working directory"

**Configure Shell:**
1. Tools → Options → Shell tab
2. Enable: "Execute in separate process"
3. Click OK

## ▶️ Run Program

### Via Thonny (Recommended)

1. File → Open → `src/deployment/main.py`
2. Click **▶️ Run** (or press **F5**)
3. Monitor output in Shell panel

**Expected output:**
```
Microphone 0 initialized successfully.
Microphone 1 initialized successfully.
...
Servo initialized successfully.
Starting object detection...
```

### Via Terminal (Alternative)
```bash
cd ~/final-project
source venv/bin/activate
python3 src/deployment/main.py
```

**Stop:** Press **Ctrl+C** (Thonny or Terminal)

## ⌨️ Useful Shortcuts

| Action | Shortcut |
|--------|----------|
| Run | F5 |
| Stop | Ctrl+C |
| Comment | Ctrl+3 |
| Uncomment | Ctrl+Shift+3 |
| Find | Ctrl+F |
| Auto-complete | Ctrl+Space |

## 🔄 Typical Workflow

**Development:**
1. Connect RealVNC
2. Open Thonny → `main.py`
3. Run (F5) → Test → Stop (Ctrl+C)
4. Edit code → Re-run

**Demo:**
1. Connect RealVNC
2. Open Thonny → Run
3. Show live detection
4. Stop when done

---

**Note:** Thonny remembers opened files, working directory, and interpreter settings for next session.
