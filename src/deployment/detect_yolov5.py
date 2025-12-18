import argparse
import os
import sys
import torch
import time
from pathlib import Path
from picamera2 import Picamera2
import numpy as np
import cv2

from models.common import DetectMultiBackend
from utils.general import (check_img_size, non_max_suppression, scale_boxes)
from utils.torch_utils import select_device

# Initialize camera
picam2 = Picamera2()
picam2.preview_configuration.main.size = (840, 840)
picam2.preview_configuration.main.format = "RGB888"
picam2.configure("preview")
picam2.start()

def run(weights='model3.torchscript', imgsz=(640, 640), conf_thres=0.25, iou_thres=0.45, device='cpu',output_queue=None):
    """
    Fungsi deteksi objek real-time menggunakan YOLOv5 dan Picamera2.

    Parameters:
    - weights: path ke model YOLOv5 .torchscript
    - imgsz: tuple ukuran input gambar
    - conf_thres: confidence threshold
    - iou_thres: IoU threshold untuk NMS
    - device: 'cpu' atau 'cuda'
    - output_queue: queue untuk mengirim label yang terdeteksi
    """
    device = select_device(device)
    weights = str(weights)  # Ensure weights is always a string

    model = DetectMultiBackend(weights, device=device)
    stride, names, pt = model.stride, model.names, model.pt
    imgsz = check_img_size(imgsz, s=stride)

    detected_label = None  # Set default sebelum loop
    print ("[INFO] Object detection started.")

    while True:
        frame = picam2.capture_array()
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        frame = cv2.resize(frame, (imgsz[1], imgsz[0]))  # Resize frame to model input size

        im = torch.from_numpy(frame).to(device)
        im = im.permute(2, 0, 1).unsqueeze(0)  # Convert from HWC to CHW format
        im = im.half() if model.fp16 else im.float()
        im /= 255  # Normalize to [0,1]

        # Inference
        pred = model(im)
        pred = non_max_suppression(pred, conf_thres, iou_thres)

        # Process predictions
        for det in pred:
            if len(det):
                det[:, :4] = scale_boxes(im.shape[2:], det[:, :4], frame.shape).round()
                for *xyxy, conf, cls in reversed(det):
                    c = int(cls)
                    label = f'{names[c]} {conf:.2f}'
                    detected_label = names[c] 
                    cv2.rectangle(frame, (int(xyxy[0]), int(xyxy[1])), (int(xyxy[2]), int(xyxy[3])), (0, 255, 0), 2)
                    cv2.putText(frame, label, (int(xyxy[0]), int(xyxy[1]) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2) 
                    output_queue.put(detected_label)   
        
        # Show frame
        cv2.imshow('YOLOv5 Detection', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        time.sleep(1)

cv2.destroyAllWindows()

def parse_opt():
    parser = argparse.ArgumentParser()
    parser.add_argument('--weights', type=str, default='model3.torchscript', help='model path')
    parser.add_argument('--imgsz', nargs='+', type=int, default=[640, 640], help='inference size h,w')
    parser.add_argument('--conf-thres', type=float, default=0.25, help='confidence threshold')
    parser.add_argument('--iou-thres', type=float, default=0.45, help='NMS IoU threshold')
    parser.add_argument('--device', default='cpu', help='cuda device or cpu')
    return parser.parse_args()

if __name__ == '__main__':
    opt = parse_opt()
    run(**vars(opt))