# 🎬 Media Organizer – Detection, Sorting, and Media Editing

An automated tool that uses AI to detect objects in photos and videos, sorts them into folders based on content, and edits videos (removes static scenes and dark shots).

---

## 📋 Contents

- ✨ Features  
- 🔧 Requirements  
- 📦 Installation  
- 🚀 Usage  
- 📁 Output Structure  
- 🐛 Troubleshooting  
- ⚙️ Customization  
- 📄 License  

---

## ✨ Features

- Object detection (people, animals, cars, furniture, electronics…)
- Automatic media sorting into categories
- Quality checking (blur, dark frames)
- Video editing (removal of static scenes)
- Keeps original files intact
- Detailed JSON detection logs
- Fully local processing (no cloud)
- Optimized for macOS (Apple Silicon / Intel)

---

## 🔧 Requirements

- Python 3.8+ (recommended 3.10+)
- Linux/macOS + Homebrew
- ~2 GB free space (YOLO model)
- Input photos and videos

---

## 📦 Installation

### 1) Clone project

```bash
git clone <your-repo>
cd media_organizer_project
```

### 2) Create virtual environment

```bash
python -m venv myvenv
source myvenv/bin/activate
```

### 3) Install FFmpeg

```bash
brew install ffmpeg
```

### 4) Install Python dependencies

```bash
pip3 install -r requirements.txt
```

---

## 🚀 Usage

```bash
python3 main.py
```

Output structure:

```bash
~/Documents/media_organizer/
├── input/
├── output_original/
├── output_edited/
└── .cache/
```

👉 Put your files into `input/` and run the script.

---

## 📁 Output Structure

```bash
output_original/
├── people/
├── animals/
├── transport/
├── furniture/
├── electronics/
├── education/
├── objects/
├── accessories/
└── rejected_bad_quality/
```

```bash
output_edited/
├── people/
├── animals/
├── transport/
└── ...
```

---

## 🐛 Troubleshooting

Missing dependency:
```bash
pip install [module name]
```

Common packages:
```bash
pip3 install ultralytics opencv-python pillow numpy torch tqdm
```

FFmpeg:
```bash
brew install ffmpeg
```

Create input folder:
```bash
mkdir -p ~/Documents/media_organizer/input
```

YOLO test:
```bash
python3 -c "from ultralytics import YOLO; YOLO('yolov8n.pt')"
```

---

## ⚙️ Customization

### config.py

```python
QUALITY_THRESHOLDS = {
    "brightness_min": 30,
    "blur_threshold": 100,
    "min_motion_frames": 5,
    "motion_threshold": 2.0,
}
```

### Supported formats

```python
SUPPORTED_IMAGES = {".jpg", ".jpeg", ".png", ".bmp", ".gif", ".webp"}
SUPPORTED_VIDEOS = {".mp4", ".avi", ".mov", ".mkv", ".flv", ".wmv", ".webm"}
```

### Confidence

```python
CONFIDENCE_THRESHOLD = 0.5
```

---

## 🎓 How it works

1. Loads YOLO model  
2. Scans input folder  
3. Detects objects in images  
4. Analyzes videos (motion + scenes)  
5. Sorts into categories  
6. Creates edited videos  
7. Saves JSON logs  

---

## 🔐 Privacy

- no cloud  
- no data upload  
- everything runs locally  

---

## 🚀 Future versions

- Web UI  
- GPU acceleration  
- Duplicate detection  
- Video compression  
- Custom AI categories  

---

## 🧠 Issues

If something doesn’t work, open an Issue in the repository.
