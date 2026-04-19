import cv2
import json
import numpy as np
from pathlib import Path
from ultralytics import YOLO
from tqdm import tqdm
import config

class ObjectDetector:
    def __init__(self):
        """Inicializuj YOLO model"""
        print(f"🔄 Načítám model {config.YOLO_MODEL}...")
        self.model = YOLO(config.YOLO_MODEL)
        self.device = "cpu"  # macOS - CPU
        print("✅ Model načten")
    
    def detect_image(self, image_path):
        """
        Detekuj objekty na obrázku.
        Vrátí seznam {objekt: počet, ...}
        """
        try:
            img = cv2.imread(str(image_path))
            if img is None:
                return None, []
            
            # YOLO detekce
            results = self.model(img, verbose=False, conf=config.CONFIDENCE_THRESHOLD, device=self.device)
            
            # Spočítej objekty
            detections = {}
            detected_objects = []
            
            if results[0].boxes is not None:
                for box in results[0].boxes:
                    class_id = int(box.cls[0])
                    class_name = config.COCO_CLASSES[class_id]
                    detections[class_name] = detections.get(class_name, 0) + 1
                    detected_objects.append(class_name)
            
            return detections, detected_objects
        
        except Exception as e:
            print(f"❌ Chyba při detekci {image_path}: {e}")
            return None, []
    
    def detect_video(self, video_path, sample_rate=5):
        """
        Detekuj objekty na videu (každý N-tý frame).
        sample_rate=5 znamená každý 5. frame.
        Vrátí {objekt: počet_výskytů, ...}
        """
        try:
            cap = cv2.VideoCapture(str(video_path))
            if not cap.isOpened():
                print(f"❌ Nemohu otevřít video: {video_path}")
                return None, []
            
            frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            detections = {}
            detected_objects = []
            frame_idx = 0
            
            print(f"   📹 Analyzuji {frame_count} snímků...")
            
            while True:
                ret, frame = cap.read()
                if not ret:
                    break
                
                # Vzorkuj: čti jen každý sample_rate-tý frame
                if frame_idx % sample_rate == 0:
                    results = self.model(frame, verbose=False, conf=config.CONFIDENCE_THRESHOLD, device=self.device)
                    
                    if results[0].boxes is not None:
                        for box in results[0].boxes:
                            class_id = int(box.cls[0])
                            class_name = config.COCO_CLASSES[class_id]
                            detections[class_name] = detections.get(class_name, 0) + 1
                            if class_name not in detected_objects:
                                detected_objects.append(class_name)
                
                frame_idx += 1
            
            cap.release()
            return detections, detected_objects
        
        except Exception as e:
            print(f"❌ Chyba při detekci videa {video_path}: {e}")
            return None, []
    
    def categorize_by_objects(self, detections):
        """
        Na základě detekovaných objektů vrátí primární kategorii.
        Např. pokud vidím "person" + "chair", bude to "people"
        """
        if not detections:
            return "other"
        
        # Mapování tříd na kategorie
        category_map = {
            "person": "people",
            "bicycle": "transport",
            "car": "transport",
            "motorcycle": "transport",
            "bus": "transport",
            "train": "transport",
            "airplane": "transport",
            "boat": "transport",
            "cat": "animals",
            "dog": "animals",
            "horse": "animals",
            "sheep": "animals",
            "cow": "animals",
            "elephant": "animals",
            "bear": "animals",
            "zebra": "animals",
            "giraffe": "animals",
            "bottle": "objects",
            "cup": "objects",
            "fork": "objects",
            "knife": "objects",
            "spoon": "objects",
            "bowl": "objects",
            "chair": "furniture",
            "couch": "furniture",
            "bed": "furniture",
            "table": "furniture",
            "dining table": "furniture",
            "laptop": "electronics",
            "tv": "electronics",
            "microwave": "electronics",
            "book": "education",
            "backpack": "accessories",
        }
        
        # Hledej nejvíce specifickou kategorii
        for obj in detections.keys():
            if obj in category_map:
                return category_map[obj]
        
        # Pokud nic speciálního, vrátí "other"
        return "other"
