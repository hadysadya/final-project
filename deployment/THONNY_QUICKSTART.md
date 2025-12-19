# 🎨 Quick Start Guide - Thonny IDE Workflow

## 📌 Overview

This guide is specifically for running the Emergency Vehicle Detection System using Thonny IDE on a Raspberry Pi 5 accessed via RealVNC Viewer.

## 🖥️ Setup Environment

### 1. Access Raspberry Pi via RealVNC

```
Laptop → RealVNC Viewer → Raspberry Pi 5 Desktop
```

**RealVNC Connection:**
- Address: `192.168.137.66`
- Username: `admin`
- Password: `admin`

### 2. Open Thonny IDE

**Location:** Applications Menu → Programming → Thonny Python IDE

## ⚙️ Thonny Configuration (One-time Setup)

### Step 1: Set Python Interpreter

1. **Tools → Options**
2. Tab **"Interpreter"**
3. Choose: **"Alternative Python 3 interpreter"**
4. Browse to: `/home/admin/hadysadya/yolo_object/bin/python3`
5. Click **OK**

**Verify:**
- Look at the bottom-right Thonny: Should show `Python 3.11.2`

### Step 2: Set Working Directory

1. **View → Files** (to open the file browser)
2. Navigate to: `/home/admin/hadysadya/final-project`
3. Right-click folder → **"Set as working directory"**

### Step 3: Configure Shell

1. **Tools → Options**
2. Tab **"Shell"**
3. ✅ Enable: "Execute in separate process"
4. Click **OK**

## 📁 Project Structure in Thonny

```
📂 /home/admin/hadysadya/final-project/
├── 📂 src/
│   └── 📂 deployment/
│       ├── 📄 main.py            ← ▶️ RUN THIS FILE
│       ├── 📄 detect_yolov5.py
│       ├── 📄 traffic_control.py
│       └── 📄 globals.py
├── 📂 models/
│   └── 📄 best.torchscript       ← Model file (7MB)
```

## ▶️ How to Run the Program

### Method 1: Run via Thonny (Recommended)

1. **Open Main File:**
   - File → Open
   - Navigate: `src/deployment/main.py`

2. **Run Program:**
   - Click the button **▶️ Run** (or press **F5**)
   - Or: Run → Run current script

3. **Monitor Output:**
   - The output will appear in **Shell** (bottom panel)
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

If you prefer terminal:

1. **Open Terminal** on Raspberry Pi Desktop
2. **Navigate & Activate venv:**
   ```bash
   cd /home/admin/hadysadya/final-project
   source ../yolo_object/bin/activate
   ```
3. **Run:**
   ```bash
   python3 src/deployment/main.py
   ```

## 🛑 How to Stop a Program

### Stop via Thonny:
- Click the button **🛑 Stop** (or press **Ctrl+C**)
- Or: Run → Interrupt execution

### Stop via Terminal:
- Press **Ctrl+C**

**Note:** The program will cleanup threads with graceful shutdown.

## 💡 Tips & Tricks

### Tip 1: Multiple Files Open

- Use **tabs** at top to switch between files
- File → Open recent → Quick access to recent files

### Tip 2: Split View

- View → Split view → Edit two files side-by-side

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

## 🔄 Typical Workflow

### Daily Development Cycle:

1. Connect via RealVNC to Raspberry Pi
2. Open Thonny IDE
3. Open `main.py` (usually auto-opens from last session)
4. Run program (F5)
5. Test hardware (mic, camera, servo, lights)
6. Monitor output in Shell
7. Make adjustments if needed
8. Re-run to test changes
9. Stop program (Ctrl+C) when done

### Demo/Presentation:

1. Connect RealVNC
2. Open Thonny
3. Open `main.py`
4. Click Run ▶️
5. Show live detection on screen
6. Trigger emergency (test with audio/vehicle)
7. Observe traffic light control
8. Stop when demo complete

## 📝 Notes

- **VNC Lag:** If video preview lags, consider disabling CV2 window

- **Long Running:** For extended testing, use Terminal instead of Thonny to avoid IDE overhead

- **Multiple Runs:** Stop program completely before re-running to avoid GPIO conflicts

---

**Happy Coding! 🚀**
