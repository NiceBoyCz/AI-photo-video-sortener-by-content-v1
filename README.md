# 🎬 Media Organizer – Detekce, Třídění a Editace Médií

Automatický nástroj, který pomocí AI detekuje objekty ve fotkách a videích, třídí je do složek podle obsahu a upravuje videa (odstraňuje statické scény a tmavé záběry).

---

## 📋 Obsah

- ✨ Funkce  
- 🔧 Požadavky  
- 📦 Instalace  
- 🚀 Použití  
- 📁 Struktura výstupu  
- 🐛 Řešení problémů  
- ⚙️ Přizpůsobení  
- 📄 Licence  

---

## ✨ Funkce

- Detekce objektů (lidé, zvířata, auta, nábytek, elektronika…)
- Automatické třídění médií do kategorií
- Kontrola kvality (rozmazání, tmavé snímky)
- Editace videí (odstranění statických scén)
- Zachování originálních souborů
- Detailní JSON log detekcí
- Plně lokální zpracování (žádný cloud)
- Optimalizace pro macOS (Apple Silicon / Intel)

---

## 🔧 Požadavky

- Python 3.8+ (doporučeno 3.10+)
- Linux/macOS + Homebrew
- ~2 GB volného místa (YOLO model)
- vstupní fotky a videa

---

## 📦 Instalace

### 1) Stažení projektu

```bash
git clone <tvůj-repo>
cd media_organizer_project
```

### 2) Vytvoření a aktivace venv

```bash
python -m venv myvenv
source /myvenv/bin/activate
```

### 3) FFmpeg

```bash
brew install ffmpeg
```

### 4) Python knihovny

```bash
pip3 install -r requirements.txt
```

---

## 🚀 Použití

```bash
python3 main.py
```

Vytvoří se:

```
~/Documents/media_organizer/
├── input/
├── output_original/
├── output_edited/
└── .cache/
```

👉 Vlož soubory do `input/` a spusť program.

---

## 📁 Struktura výstupu

```
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

```
output_edited/
├── people/
├── animals/
├── transport/
└── ...
```

## 🐛 Řešení problémů

### Nelalezená python knihovna nebo závislost
```bash
pip install [název modulu/závislosti]
```

### Missing modul
```bash
pip3 install ultralytics opencv-python pillow numpy torch tqdm
```

### ffmpeg
```bash
brew install ffmpeg
```

### input složka
```bash
mkdir -p ~/Documents/media_organizer/input
```

### YOLO model
```bash
python3 -c "from ultralytics import YOLO; YOLO('yolov8n.pt')"
```

---

## ⚙️ Přizpůsobení

### config.py

```python
QUALITY_THRESHOLDS = {
    "brightness_min": 30,
    "blur_threshold": 100,
    "min_motion_frames": 5,
    "motion_threshold": 2.0,
}
```

### Formáty

```python
SUPPORTED_IMAGES = {".jpg", ".jpeg", ".png", ".bmp", ".gif", ".webp"}
SUPPORTED_VIDEOS = {".mp4", ".avi", ".mov", ".mkv", ".flv", ".wmv", ".webm"}
```

### Confidence

```python
CONFIDENCE_THRESHOLD = 0.5
```

---

## 🎓 Jak to funguje

1. Načte YOLO model  
2. Projde `input/` složku  
3. Detekuje objekty ve fotkách  
4. Analyzuje videa (pohyb + scény)  
5. Třídí do kategorií  
6. Vytvoří upravená videa  
7. Uloží JSON log  

---

## 📊 Příklad logu

```json
{
  "foto.jpg": {
    "type": "image",
    "category": "people",
    "detections": {
      "person": 3
    }
  }
}
```

---

## 🔐 Soukromí

- žádný cloud  
- žádné odesílání dat  
- vše běží lokálně  


## 🚀 Budoucí verze

- Web UI  
- GPU akcelerace  
- Duplicate detection  
- Komprese videí  
- Vlastní AI kategorie

## Pokud jsou jakékoli problémy nebo používate jakoukoli jinou Linux distribuci na které to nefunguje, napište do Issues.
