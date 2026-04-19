import cv2
import numpy as np
from pathlib import Path
import subprocess
import config

class VideoEditor:
    """Editace videí - ořezávání, odstranění špatných částí"""
    
    @staticmethod
    def cut_static_scenes(input_video, output_video, static_ranges):
        """
        Vyrež statické části z videa.
        static_ranges: seznam dict s "start_frame", "end_frame"
        """
        try:
            cap = cv2.VideoCapture(str(input_video))
            if not cap.isOpened():
                print(f"❌ Nemohu otevřít video: {input_video}")
                return False
            
            fps = cap.get(cv2.CAP_PROP_FPS)
            width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            
            # Vytvoř writer pro výstup
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            out = cv2.VideoWriter(str(output_video), fourcc, fps, (width, height))
            
            frame_idx = 0
            frames_to_skip = set()
            
            # Postav set všech framů, které se mají přeskočit
            for static_range in static_ranges:
                for f in range(static_range["start_frame"], static_range["end_frame"]):
                    frames_to_skip.add(f)
            
            total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            
            while True:
                ret, frame = cap.read()
                if not ret:
                    break
                
                # Pokud frame NENÍ ve "skip" seznamu, napi ho
                if frame_idx not in frames_to_skip:
                    out.write(frame)
                
                frame_idx += 1
            
            cap.release()
            out.release()
            
            print(f"   ✅ Ořezané video uloženo: {output_video}")
            return True
        
        except Exception as e:
            print(f"❌ Chyba při ořezávání videa: {e}")
            return False
    
    @staticmethod
    def cut_by_brightness(input_video, output_video, brightness_threshold=30):
        """
        Vyrež příliš tmavé části videa.
        """
        try:
            cap = cv2.VideoCapture(str(input_video))
            if not cap.isOpened():
                return False
            
            fps = cap.get(cv2.CAP_PROP_FPS)
            width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            out = cv2.VideoWriter(str(output_video), fourcc, fps, (width, height))
            
            while True:
                ret, frame = cap.read()
                if not ret:
                    break
                
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                brightness = np.mean(gray)
                
                # Pokud je dostatečně jasný, napi ho
                if brightness >= brightness_threshold:
                    out.write(frame)
            
            cap.release()
            out.release()
            
            print(f"   ✅ Video bez tmavých částí: {output_video}")
            return True
        
        except Exception as e:
            print(f"❌ Chyba: {e}")
            return False
    
    @staticmethod
    def combine_filters(input_video, output_video, quality_info, motion_info):
        """
        Kombinuj všechny filtry najednou:
        - Odstraň statické scény
        - Odstraň tmavé záběry
        """
        try:
            cap = cv2.VideoCapture(str(input_video))
            if not cap.isOpened():
                return False
            
            fps = cap.get(cv2.CAP_PROP_FPS)
            width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            out = cv2.VideoWriter(str(output_video), fourcc, fps, (width, height))
            
            # Postav set statických framů
            frames_to_skip = set()
            for static_range in motion_info.get("static_ranges", []):
                for f in range(static_range["start_frame"], static_range["end_frame"]):
                    frames_to_skip.add(f)
            
            brightness_min = config.QUALITY_THRESHOLDS["brightness_min"]
            frame_idx = 0
            
            while True:
                ret, frame = cap.read()
                if not ret:
                    break
                
                # Filtr 1: Není statický?
                if frame_idx in frames_to_skip:
                    frame_idx += 1
                    continue
                
                # Filtr 2: Je dostatečně jasný?
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                brightness = np.mean(gray)
                
                if brightness < brightness_min:
                    frame_idx += 1
                    continue
                
                # Pokud prošel všemi filtry, napi
                out.write(frame)
                frame_idx += 1
            
            cap.release()
            out.release()
            
            print(f"   ✅ Filtrované video: {output_video}")
            return True
        
        except Exception as e:
            print(f"❌ Chyba: {e}")
            return False
    
    @staticmethod
    def get_video_info(video_path):
        """Vrátí info o videu (délka, rozměry, FPS)"""
        try:
            cap = cv2.VideoCapture(str(video_path))
            fps = cap.get(cv2.CAP_PROP_FPS)
            frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            
            duration = frame_count / fps if fps > 0 else 0
            
            cap.release()
            
            return {
                "fps": fps,
                "frame_count": frame_count,
                "width": width,
                "height": height,
                "duration_sec": duration
            }
        except Exception as e:
            return {"error": str(e)}
