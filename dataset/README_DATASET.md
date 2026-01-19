# 🚨 Emergency Vehicle Dataset

Prototype dataset for emergency vehicle detection system (600 images, 6 classes).

## 📥 Download

**Google Drive**: [dataset.zip (32 MB)](https://drive.google.com/file/d/1tjjm40aE8eqMzria_FoWZeDjfFvtRSd1/view?usp=sharing)

## 📊 Statistics

| Metric | Value |
|--------|-------|
| Training images | 420 |
| Validation images | 180 |
| Total | 600 |
| Classes | 6 |
| Format | YOLO (.txt) |
| Resolution | 640x640 |

## 🏷️ Classes

| ID | Class | Type |
|----|-------|------|
| 0 | Ambulance | Emergency vehicle |
| 1 | Fire Truck | Emergency vehicle |
| 2 | Koenigsegg | Regular vehicle (baseline) |
| 3 | Mclaren | Regular vehicle (baseline) |
| 4 | Mercedes | Regular vehicle (baseline) |
| 5 | Police Car | Emergency vehicle |

**Note**: Regular vehicles (Koenigsegg, Mclaren, Mercedes) are included as baseline comparison for emergency vehicle detection.

## 📁 Directory Structure
```
dataset/
├── data.yaml
├── train/
│   ├── images/      # 420 images
│   └── labels/      # 420 labels
└── valid/
    ├── images/      # 180 images
    └── labels/      # 180 labels
```

## 📝 Label Format

YOLO format (normalized coordinates):
```
<class_id> <x_center> <y_center> <width> <height>
```

Example: `0 0.512 0.623 0.214 0.345`

All values normalized to [0.0 - 1.0].

## 🚀 Usage

**For training**: Follow `notebooks/training_notebook.ipynb`

**For deployment**: Pre-trained model included in `models/best.torchscript`

## ⚠️ Limitations

This is a **proof-of-concept dataset**:

- Limited size (600 images - production requires 5,000+)
- Limited weather/lighting conditions
- Not suitable for production deployment
- Sufficient for prototype demonstration only

## 📄 License

Educational/Research use only.

---

Version 1.0 | July 2025
