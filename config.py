import os
from pathlib import Path

# ============ CESTY ============
BASE_DIR = Path.home() / "Documents" / "media_organizer"
INPUT_DIR = BASE_DIR / "input"
OUTPUT_ORIGINAL = BASE_DIR / "output_original"
OUTPUT_EDITED = BASE_DIR / "output_edited"
CACHE_DIR = BASE_DIR / ".cache"
DETECTIONS_LOG = CACHE_DIR / "detections.json"

# Vytvoř všechny složky, pokud neexistují
for directory in [INPUT_DIR, OUTPUT_ORIGINAL, OUTPUT_EDITED, CACHE_DIR]:
    directory.mkdir(parents=True, exist_ok=True)

# ============ YOLO MODEL ============
YOLO_MODEL = "yolov8n.pt"  # nano - nejrychlejší na CPU

# ============ KVALITA VIDEA ============
QUALITY_THRESHOLDS = {
    "brightness_min": 30,      # Pokud je průměrný jas nižší, je video/foto "tmavé"
    "blur_threshold": 100,     # Pokud je Laplaceův rozptyl nižší, je "rozmazané"
    "min_motion_frames": 5,    # Při ořezávání: když je méně než X rámců s pohybem, vyrež
    "motion_threshold": 2.0,   # Citlivost detekce pohybu (procenta změny pixelů)
}

# ============ COCO TŘÍDY (YOLO detekuje všechno) ============
COCO_CLASSES = [
    "person", "bicycle", "car", "motorcycle", "airplane", "bus", "train", "truck",
    "boat", "traffic light", "fire hydrant", "stop sign", "parking meter", "bench",
    "cat", "dog", "horse", "sheep", "cow", "elephant", "bear", "zebra", "giraffe",
    "backpack", "umbrella", "handbag", "tie", "suitcase", "frisbee", "skis",
    "snowboard", "sports ball", "kite", "baseball bat", "baseball glove", "skateboard",
    "surfboard", "tennis racket", "bottle", "wine glass", "cup", "fork", "knife",
    "spoon", "bowl", "banana", "apple", "sandwich", "orange", "broccoli", "carrot",
    "hot dog", "pizza", "donut", "cake", "chair", "couch", "potted plant", "bed",
    "dining table", "toilet", "tv", "laptop", "mouse", "remote", "keyboard", "microwave",
    "oven", "toaster", "sink", "refrigerator", "book", "clock", "vase", "scissors",
    "teddy bear", "hair drier", "toothbrush"
]

# ============ FORMÁTY ============
SUPPORTED_IMAGES = {".jpg", ".jpeg", ".png", ".bmp", ".gif", ".webp"}
SUPPORTED_VIDEOS = {".mp4", ".avi", ".mov", ".mkv", ".flv", ".wmv", ".webm"}

# ============ OSTATNÍ ============
BATCH_SIZE = 1  # CPU nesnese víc
CONFIDENCE_THRESHOLD = 0.5  # YOLO confidence (0-1)
