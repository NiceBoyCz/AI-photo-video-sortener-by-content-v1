import json
import shutil
from pathlib import Path
from tqdm import tqdm
import config

class MediaOrganizer:
    """Třídění médií do složek podle kategorií"""
    
    def __init__(self):
        self.detections_log = {}
    
    def organize_originals(self, detector, quality_checker):
        """
        Třídí ORIGINÁLNÍ fotky a videa do:
        output_original/
        ├── people/
        ├── animals/
        ├── transport/
        ├── furniture/
        ├── electronics/
        ├── other/
        └── rejected_bad_quality/
        """
        print("\n📂 TŘÍDÍM ORIGINÁLNÍ MÉDIA...")
        
        all_files = []
        
        # Sesbírej všechny fotky a videa
        for ext in config.SUPPORTED_IMAGES:
            all_files.extend(config.INPUT_DIR.glob(f"*{ext}"))
            all_files.extend(config.INPUT_DIR.glob(f"*{ext.upper()}"))
        
        for ext in config.SUPPORTED_VIDEOS:
            all_files.extend(config.INPUT_DIR.glob(f"*{ext}"))
            all_files.extend(config.INPUT_DIR.glob(f"*{ext.upper()}"))
        
        if not all_files:
            print("⚠️ V INPUT_DIR nenalezeny žádné soubory!")
            return
        
        print(f"📦 Nalezeno {len(all_files)} souborů\n")
        
        # Projdi každý soubor
        for file_path in tqdm(all_files, desc="Třídím originály"):
            file_path = Path(file_path)
            
            # Určí, jestli je to fotka nebo video
            is_image = file_path.suffix.lower() in config.SUPPORTED_IMAGES
            is_video = file_path.suffix.lower() in config.SUPPORTED_VIDEOS
            
            category = "other"
            quality_ok = True
            reason = ""
            detected_objects = []
            
            # KONTROLA KVALITY
            if is_image:
                quality_info = quality_checker.check_image_quality(file_path)
                quality_ok = quality_info["is_good"]
                reason = quality_info["reason"]
                
                # DETEKCE OBJEKTŮ
                if quality_ok:
                    detections, detected_objects = detector.detect_image(file_path)
                    if detections:
                        category = detector.categorize_by_objects(detections)
                    
                    self.detections_log[str(file_path)] = {
                        "type": "image",
                        "category": category,
                        "detections": detections,
                        "quality": quality_info
                    }
            
            elif is_video:
                quality_info = quality_checker.check_video_quality(file_path)
                quality_ok = quality_info["is_good"]
                reason = quality_info["reason"]
                
                # DETEKCE OBJEKTŮ
                if quality_ok:
                    detections, detected_objects = detector.detect_video(file_path)
                    if detections:
                        category = detector.categorize_by_objects(detections)
                    
                    motion_info = quality_checker.check_motion_in_video(file_path)
                    
                    self.detections_log[str(file_path)] = {
                        "type": "video",
                        "category": category,
                        "detections": detections,
                        "quality": quality_info,
                        "motion": motion_info
                    }
            
            # ROZHODNUTÍ: KDE UMÍSTIT
            if not quality_ok:
                target_dir = config.OUTPUT_ORIGINAL / "rejected_bad_quality"
            else:
                target_dir = config.OUTPUT_ORIGINAL / category
            
            target_dir.mkdir(parents=True, exist_ok=True)
            target_path = target_dir / file_path.name
            
            # Kopíruj soubor (ne přesuň - zachováme originál)
            try:
                shutil.copy2(file_path, target_path)
            except Exception as e:
                print(f"❌ Chyba při kopírování {file_path}: {e}")
        
        print(f"\n✅ Originály organizovány do {config.OUTPUT_ORIGINAL}")
        
        # Ulož detekční log
        self._save_detection_log()
    
    def organize_edited(self, detector, quality_checker, video_editor):
        """
        Vezmi ORIGINÁLNÍ soubory a vytvoř EDITED verze:
        output_edited/
        ├── people/
        ├── animals/
        ├── transport/
        └── ... (stejné kategorie)
        
        VIDEA se ořežou (bez statických scén, bez tmavých částí)
        FOTKY se jen zkopírují (nelze editovat fotky bez pohybu)
        """
        print("\n✂️ VYTVÁŘÍM EDITOVANÉ VERZE...\n")
        
        # Projdi všechny organizované soubory
        for category_dir in config.OUTPUT_ORIGINAL.iterdir():
            if not category_dir.is_dir() or category_dir.name == "rejected_bad_quality":
                continue
            
            print(f"\n📁 Kategorie: {category_dir.name}")
            
            for file_path in tqdm(list(category_dir.iterdir()), desc=f"  Edituji {category_dir.name}"):
                if not file_path.is_file():
                    continue
                
                is_video = file_path.suffix.lower() in config.SUPPORTED_VIDEOS
                is_image = file_path.suffix.lower() in config.SUPPORTED_IMAGES
                
                # Vytvoř cílový adresář
                target_dir = config.OUTPUT_EDITED / category_dir.name
                target_dir.mkdir(parents=True, exist_ok=True)
                
                if is_image:
                    # Fotky se jen kopírují (žádná editace)
                    target_path = target_dir / file_path.name
                    try:
                        shutil.copy2(file_path, target_path)
                    except Exception as e:
                        print(f"  ❌ Chyba: {e}")
                
                elif is_video:
                    # Videa se editují
                    motion_info = quality_checker.check_motion_in_video(file_path)
                    quality_info = quality_checker.check_video_quality(file_path)
                    
                    # Vytvoř název edited souboru
                    target_path = target_dir / f"{file_path.stem}_edited.mp4"
                    
                    # Aplikuj všechny filtry
                    success = video_editor.combine_filters(
                        file_path,
                        target_path,
                        quality_info,
                        motion_info
                    )
                    
                    if not success:
                        # Pokud editace selhala, zkopíruj originál
                        try:
                            shutil.copy2(file_path, target_dir / file_path.name)
                        except Exception as e:
                            print(f"  ❌ Chyba: {e}")
        
        print(f"\n✅ Editované verze vytvořeny v {config.OUTPUT_EDITED}")
    
    def _save_detection_log(self):
        """Ulož JSON log s detekcemi"""
        try:
            # Konvertuj Path objekty na stringy pro JSON
            log_data = {}
            for key, value in self.detections_log.items():
                log_data[str(key)] = value
            
            with open(config.DETECTIONS_LOG, "w", encoding="utf-8") as f:
                json.dump(log_data, f, indent=2, ensure_ascii=False)
            
            print(f"\n📋 Log detekací uložen: {config.DETECTIONS_LOG}")
        
        except Exception as e:
            print(f"❌ Chyba při ukládání logu: {e}")
    
    def print_summary(self):
        """Vytiskni shrnutí třídění"""
        print("\n" + "="*60)
        print("📊 SHRNUTÍ TŘÍDĚNÍ")
        print("="*60)
        
        # Počet souborů v každé kategorii
        categories = {}
        
        for category_dir in config.OUTPUT_ORIGINAL.iterdir():
            if category_dir.is_dir():
                count = len(list(category_dir.glob("*")))
                categories[category_dir.name] = count
        
        for cat, count in sorted(categories.items(), key=lambda x: x[1], reverse=True):
            print(f"  {cat:.<40} {count:>3} souborů")
        
        print("="*60 + "\n")
