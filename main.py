#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
from pathlib import Path
import config
from detector import ObjectDetector
from quality_check import QualityChecker
from video_editor import VideoEditor
from organizer import MediaOrganizer

def main():
    """
    Hlavní program:
    1. Detekuje objekty
    2. Kontroluje kvalitu
    3. Třídí média do složek
    4. Edituje videa (ořezává)
    """
    
    print("\n" + "="*60)
    print("🎬 MEDIA ORGANIZER - Detekce, Třídění, Editace")
    print("="*60 + "\n")
    
    # Kontrola: existují vstupní soubory?
    input_files = list(config.INPUT_DIR.glob("*"))
    input_files = [f for f in input_files if f.is_file()]
    
    if not input_files:
        print(f"❌ CHYBA: V {config.INPUT_DIR} nejsou žádné soubory!")
        print(f"   Vlož fotky/videa do: {config.INPUT_DIR}")
        sys.exit(1)
    
    print(f"✅ Input složka: {config.INPUT_DIR}")
    print(f"✅ Output originály: {config.OUTPUT_ORIGINAL}")
    print(f"✅ Output editované: {config.OUTPUT_EDITED}\n")
    
    # ============ KROK 1: NAČTENÍ MODELU ============
    print("KROK 1️⃣: Inicializace detektoru")
    print("-" * 60)
    detector = ObjectDetector()
    quality_checker = QualityChecker()
    video_editor = VideoEditor()
    organizer = MediaOrganizer()
    
    # ============ KROK 2: TŘÍDĚNÍ ORIGINÁLŮ ============
    print("\nKROK 2️⃣: Třídění originálních souborů")
    print("-" * 60)
    organizer.organize_originals(detector, quality_checker)
    
    # ============ KROK 3: VYTVÁŘENÍ EDITOVANÝCH VERZÍ ============
    print("\nKROK 3️⃣: Vytváření editovaných verzí")
    print("-" * 60)
    organizer.organize_edited(detector, quality_checker, video_editor)
    
    # ============ KROK 4: SHRNUTÍ ============
    print("\nKROK 4️⃣: Výsledky")
    print("-" * 60)
    organizer.print_summary()
    
    print("\n✅ HOTOVO!")
    print(f"\n📁 Otevři si výsledky:")
    print(f"   Originály: {config.OUTPUT_ORIGINAL}")
    print(f"   Editované: {config.OUTPUT_EDITED}")
    print(f"   Log:       {config.DETECTIONS_LOG}\n")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️ Přerušeno uživatelem")
        sys.exit(0)
    except Exception as e:
        print(f"\n\n❌ CHYBA: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
