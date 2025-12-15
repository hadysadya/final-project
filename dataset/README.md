# Download Full Dataset

⚠️ **This folder contains sample files for preview only.**

## Full Dataset

📦 **Download from Google Drive**: [Click here](https://drive.google.com/file/d/1tjjm40aE8eqMzria_FoWZeDjfFvtRSd1/view?usp=sharing) 

## Dataset Information
- **Train**: 420 images + 420 labels
- **Valid**: 180 images + 180 labels
- **Format**: YOLO format
- **File**: data.yaml, README files included

## Complete Structure
```
dataset/
├── data.yaml
├── README.dataset.txt
├── README.roboflow.txt
├── train/
│   ├── images/     # 420 file .jpg
│   └── labels/     # 420 file .txt
└── valid/
    ├── images/     # 180 file .jpg
    └── labels/     # 180 file .txt
```

Total: 600 images + 600 labels + 3 files = 1203 files

## How to Use
1. Download `dataset.zip` from the link above
2. Extract it into the root folder of your project
3. Run training: `python train.py --data dataset/data.yaml`
