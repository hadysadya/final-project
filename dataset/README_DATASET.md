# 🚨 Emergency Vehicle Dataset - Prototype

⚠️ **This is a prototype-scale dataset for proof-of-concept demonstration.**

## 📦 Download Dataset

**Google Drive**: [Download dataset.zip](https://drive.google.com/file/d/1tjjm40aE8eqMzria_FoWZeDjfFvtRSd1/view?usp=sharing)

## 📊 Dataset Info

| Item | Count |
|------|-------|
| Training | 420 Images |
| Validation | 180 Images |
| Total | 600 Images |
| Classes | 6 (Ambulance, Fire Truck, etc.) |
| Format | YOLO (.txt labels) |

**Note**: This is a prototype dataset sufficient for demonstration and initial testing. For production deployment, a larger and more diverse dataset is recommended.

## 📁 Structure

```
dataset/
├── data.yaml                  # Config file
├── README.dataset.txt         # Dataset metadata
├── README.roboflow.txt        # Roboflow export info
├── train/
│   ├── images/                # 420 training images
│   └── labels/                # 420 YOLO labels
└── valid/
    ├── images/                # 180 validation images
    └── labels/                # 180 YOLO labels
```

## 🚀 Usage

### For Deployment (Current Prototype):
```bash
# Dataset NOT needed - pre-trained model included
# Just run: python3 src/deployment/main.py
```

## 📝 Label Format (YOLO)

```
<class_id> <x_center> <y_center> <width> <height>
```

- 0 = Ambulance  
- 1 = Fire Truck
- . . . . . 
- 5 = Police Car

All coordinates normalized to [0, 1].

## ⚠️ Prototype Limitations

This dataset is designed for **proof-of-concept** and has limitations:

- ❌ Limited variety (600 images only)
- ❌ May not cover all lighting conditions
- ❌ May not cover all vehicle types/angles
- ❌ Not suitable for production deployment
- ✅ Sufficient for prototype demonstration
- ✅ Good for initial model testing

**For Production**: Expand to 5,000+ images with diverse conditions.

## 📄 License

**Prototype/Educational Use Only**

---

**Version**: 1.0 (Prototype) | **Date**: July 2025