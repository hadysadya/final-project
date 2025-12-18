# 📦 Migration Guide - Memindahkan Code ke Struktur Baru

## 🎯 Tujuan
Memindahkan code existing dari `/home/admin/TAedward/yolov5` ke struktur repository `final-project` yang lebih terorganisir.

---

## 📂 Struktur Sebelum & Sesudah

### Sebelum (Existing):
```
/home/admin/TAedward/yolov5/
├── programbaru2.py          # Main program
├── detectyolov5.py          # YOLO detection
├── lalulintas.py            # Traffic control
├── globals.py               # Global variables
├── model3.torchscript       # Model file
├── models/                  # YOLOv5 models folder
└── utils/                   # YOLOv5 utils folder
```

### Sesudah (New Structure):
```
/home/admin/TAedward/final-project/
├── src/
│   └── deployment/
│       ├── __init__.py              ✅ Sudah ada
│       ├── config.py                ✅ Sudah ada
│       ├── main.py                  ⬅️ dari programbaru2.py
│       ├── detect_yolov5.py         ⬅️ dari detectyolov5.py
│       ├── traffic_control.py       ⬅️ dari lalulintas.py
│       └── globals.py               ⬅️ dari globals.py
├── models/
│   └── model3.torchscript           ⬅️ dari yolov5/
├── models/                          ⬅️ copy dari yolov5/models/
│   └── common.py
└── utils/                           ⬅️ copy dari yolov5/utils/
    ├── general.py
    └── torch_utils.py
```

---

## 🚀 Langkah-langkah Migrasi

### Step 1: Buat Struktur Folder Baru

```bash
# Buka Terminal di Raspberry Pi atau via SSH
cd /home/admin/TAedward

# Clone atau create repository final-project (jika belum ada)
# Jika sudah ada, skip langkah ini
git clone https://github.com/hadysadya/final-project.git

# Masuk ke folder
cd final-project

# Buat struktur folder deployment
mkdir -p src/deployment
mkdir -p models
mkdir -p logs
```

### Step 2: Copy File Config yang Sudah Dibuat

**File-file ini sudah Anda download dari artifacts sebelumnya:**
- `__init__.py`
- `config.py`
- `main.py`
- `detect_yolov5.py`
- `traffic_control.py`
- `globals.py`

**Copy ke lokasi yang benar:**

```bash
# Dari lokasi download Anda, copy ke:
cp /path/to/download/__init__.py src/deployment/
cp /path/to/download/config.py src/deployment/
cp /path/to/download/main.py src/deployment/
cp /path/to/download/detect_yolov5.py src/deployment/
cp /path/to/download/traffic_control.py src/deployment/
cp /path/to/download/globals.py src/deployment/
```

**Atau jika lebih mudah via Thonny:**
1. Buka Thonny IDE
2. File → Open → Pilih file dari artifacts
3. File → Save As → Save ke `/home/admin/TAedward/final-project/src/deployment/`

### Step 3: Copy YOLOv5 Dependencies

```bash
# Copy YOLOv5 models folder
cp -r /home/admin/TAedward/yolov5/models /home/admin/TAedward/final-project/

# Copy YOLOv5 utils folder
cp -r /home/admin/TAedward/yolov5/utils /home/admin/TAedward/final-project/

# Copy model file
cp /home/admin/TAedward/yolov5/model3.torchscript /home/admin/TAedward/final-project/models/
```

### Step 4: Verify Structure

```bash
cd /home/admin/TAedward/final-project

# Check structure
tree -L 3
# atau
ls -R
```

Pastikan struktur seperti ini:
```
final-project/
├── src/
│   └── deployment/
│       ├── __init__.py
│       ├── config.py
│       ├── main.py
│       ├── detect_yolov5.py
│       ├── traffic_control.py
│       └── globals.py
├── models/
│   ├── common.py
│   ├── experimental.py
│   └── model3.torchscript
├── utils/
│   ├── general.py
│   ├── torch_utils.py
│   └── ...
└── logs/
```

---

## 🔧 Aktivasi Virtual Environment

### Option 1: Gunakan Virtual Environment Existing

```bash
# Aktifkan venv yang sudah ada
cd /home/admin/TAedward
source yolo_object/bin/activate

# Verifikasi Python version
python --version  # Should show 3.11.2
```

### Option 2: Buat Symlink untuk Kemudahan

```bash
# Buat symlink venv ke dalam folder final-project
cd /home/admin/TAedward/final-project
ln -s /home/admin/TAedward/yolo_object venv

# Sekarang bisa aktivasi dari folder final-project
source venv/bin/activate
```

---

## ▶️ Cara Menjalankan dengan Thonny IDE

### Setup Thonny untuk Project Baru

1. **Buka Thonny IDE**

2. **Set Interpreter ke Virtual Environment:**
   - Tools → Options → Interpreter
   - Pilih "Alternative Python 3 interpreter"
   - Browse ke: `/home/admin/TAedward/yolo_object/bin/python3`
   - Click OK

3. **Open Main Program:**
   - File → Open
   - Navigate ke: `/home/admin/TAedward/final-project/src/deployment/main.py`

4. **Run Program:**
   - Click tombol **Run** (▶️) atau tekan **F5**
   - Program akan jalan seperti biasa!

### Jika Ada Error Import

Jika muncul error `ModuleNotFoundError: No module named 'models'` atau `utils`:

**Solusi:** Tambahkan parent directory ke Python path.

Tambahkan di baris paling atas `main.py` dan `detect_yolov5.py`:

```python
import sys
from pathlib import Path

# Add project root to Python path
PROJECT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))
```

---

## 🧪 Testing

### Test 1: Import Modules

```python
# Buka Python Console di Thonny atau Terminal
cd /home/admin/TAedward/final-project
source venv/bin/activate
python3

>>> from src.deployment import config
>>> from src.deployment import globals
>>> print("Config loaded successfully!")
```

### Test 2: Check Configuration

```python
>>> from src.deployment.config import print_config_summary
>>> print_config_summary()
```

Should show:
```
======================================================================
SYSTEM CONFIGURATION SUMMARY
======================================================================

Model: /home/admin/TAedward/final-project/models/model3.torchscript
Device: cpu
Image Size: (640, 640)

Microphones: 4 devices
Audio Threshold: -40 dBFS
...
```

### Test 3: Run Main Program

```bash
cd /home/admin/TAedward/final-project
source venv/bin/activate
python3 src/deployment/main.py
```

Atau via Thonny: Open `main.py` → Click Run

---

## 🔄 Git Integration

### Push ke GitHub

```bash
cd /home/admin/TAedward/final-project

# Add semua file baru
git add src/deployment/
git add models/model3.torchscript
git add deployment/

# Commit
git commit -m "Add deployment structure and configuration"

# Push
git push origin main
```

### Update .gitignore

Buat file `.gitignore` untuk exclude file yang tidak perlu:

```bash
# Create .gitignore
cat > .gitignore << 'EOF'
# Virtual Environment
venv/
yolo_object/
__pycache__/
*.pyc

# Logs
logs/*.log
*.log

# Model files (optional - jika model terlalu besar)
# models/*.torchscript
# models/*.pt

# IDE
.vscode/
.idea/
*.swp

# System
.DS_Store
Thumbs.db

# Temporary
*.tmp
*.bak
EOF

git add .gitignore
git commit -m "Add .gitignore"
git push
```

---

## 📋 Checklist Migrasi

Gunakan checklist ini untuk memastikan semua sudah benar:

- [ ] Folder `final-project/src/deployment/` sudah dibuat
- [ ] File `__init__.py` ada di `src/deployment/`
- [ ] File `config.py` ada di `src/deployment/`
- [ ] File `main.py` ada di `src/deployment/`
- [ ] File `detect_yolov5.py` ada di `src/deployment/`
- [ ] File `traffic_control.py` ada di `src/deployment/`
- [ ] File `globals.py` ada di `src/deployment/`
- [ ] Folder `models/` sudah ada dengan `common.py` dll
- [ ] Folder `utils/` sudah ada dengan `general.py` dll
- [ ] File `model3.torchscript` ada di `models/`
- [ ] Virtual environment bisa diaktifkan
- [ ] Thonny interpreter sudah di-set ke venv
- [ ] Test import berhasil
- [ ] Program bisa dijalankan dari Thonny
- [ ] Git push berhasil (optional)

---

## 🆘 Troubleshooting

### Error: ModuleNotFoundError: No module named 'models'

**Solusi:**
```python
# Tambahkan di main.py dan detect_yolov5.py (line 1)
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
```

### Error: FileNotFoundError: model3.torchscript

**Solusi:**
```bash
# Verify model location
ls -la /home/admin/TAedward/final-project/models/model3.torchscript

# Update config.py jika perlu
# Edit YOLOV5_CONFIG['WEIGHTS']
```

### Error: Permission denied for GPIO

**Solusi:**
```bash
sudo usermod -a -G gpio admin
sudo reboot
```

### Thonny tidak bisa import config

**Solusi:**
```python
# Set working directory di Thonny
import os
os.chdir('/home/admin/TAedward/final-project')
```

---

## ✅ Selesai!

Setelah migrasi selesai, struktur code Anda akan lebih rapi dan mudah di-maintain. 

**Next Steps:**
1. Test program secara menyeluruh
2. Dokumentasikan perubahan di README.md
3. Push ke GitHub
4. Buat demo/presentation!

---

**Questions?** Silakan hubungi atau buka issue di GitHub repository.