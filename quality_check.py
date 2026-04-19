import cv2
import numpy as np
from pathlib import Path
import config

class QualityChecker:
    """Kontrola kvality obrázků a videí"""
    
    @staticmethod
    def check_image_quality(image_path):
        """
        Zkontroluj kvalitu obrázku.
        Vrátí dict s {brightness, blur, is_good}
        """
        try:
            img = cv2.imread(str(image_path))
            if img is None:
                return {"brightness": 0, "blur": 0, "is_good": False, "reason": "Nemohu otevřít"}
            
            # Převeď na grayscale
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            
            # 1. JAS (brightness)
            brightness = np.mean(gray)
            
            # 2. ROZMAZÁNÍ (Laplacian variance)
            laplacian = cv2.Laplacian(gray, cv2.CV_64F)
            blur = laplacian.var()
            
            # Rozhodnutí
            is_too_dark = brightness < config.QUALITY_THRESHOLDS["brightness_min"]
            is_too_blurry = blur < config.QUALITY_THRESHOLDS["blur_threshold"]
            
            is_good = not (is_too_dark or is_too_blurry)
            reason = ""
            
            if is_too_dark:
                reason = "příliš tmavé"
            elif is_too_blurry:
                reason = "rozmazané"
            
            return {
                "brightness": float(brightness),
                "blur": float(blur),
                "is_good": is_good,
                "reason": reason
            }
        
        except Exception as e:
            return {"brightness": 0, "blur": 0, "is_good": False, "reason": str(e)}
    
    @staticmethod
    def check_video_quality(video_path, sample_frames=10):
        """
        Zkontroluj kvalitu videa (vzorkuj N snímků).
        Vrátí průměrné hodnoty a seznam dobrých/špatnýchframes.
        """
        try:
            cap = cv2.VideoCapture(str(video_path))
            if not cap.isOpened():
                return {
                    "brightness": 0,
                    "blur": 0,
                    "is_good": False,
                    "reason": "Nemohu otevřít video"
                }
            
            frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            step = max(1, frame_count // sample_frames)
            
            brightnesses = []
            blurs = []
            frame_idx = 0
            
            while True:
                ret, frame = cap.read()
                if not ret:
                    break
                
                if frame_idx % step == 0:
                    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                    brightness = np.mean(gray)
                    laplacian = cv2.Laplacian(gray, cv2.CV_64F)
                    blur = laplacian.var()
                    
                    brightnesses.append(brightness)
                    blurs.append(blur)
                
                frame_idx += 1
            
            cap.release()
            
            avg_brightness = float(np.mean(brightnesses)) if brightnesses else 0
            avg_blur = float(np.mean(blurs)) if blurs else 0
            
            is_too_dark = avg_brightness < config.QUALITY_THRESHOLDS["brightness_min"]
            is_too_blurry = avg_blur < config.QUALITY_THRESHOLDS["blur_threshold"]
            
            is_good = not (is_too_dark or is_too_blurry)
            reason = ""
            
            if is_too_dark:
                reason = "příliš tmavé"
            elif is_too_blurry:
                reason = "rozmazané"
            
            return {
                "brightness": avg_brightness,
                "blur": avg_blur,
                "is_good": is_good,
                "reason": reason
            }
        
        except Exception as e:
            return {"brightness": 0, "blur": 0, "is_good": False, "reason": str(e)}
    
    @staticmethod
    def check_motion_in_video(video_path):
        """
        Zjisti, kolik je v videu pohybu.
        Vrátí procento frames s pohybem a seznam "statických" intervalů.
        """
        try:
            cap = cv2.VideoCapture(str(video_path))
            if not cap.isOpened():
                return {"has_motion": False, "motion_percent": 0, "static_ranges": []}
            
            frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            fps = cap.get(cv2.CAP_PROP_FPS)
            
            prev_frame = None
            moving_frames = 0
            static_start = 0
            static_ranges = []
            
            frame_idx = 0
            
            while True:
                ret, frame = cap.read()
                if not ret:
                    break
                
                # Zmenši frame pro rychlost
                frame_small = cv2.resize(frame, (320, 240))
                gray = cv2.cvtColor(frame_small, cv2.COLOR_BGR2GRAY)
                
                if prev_frame is not None:
                    # Spočítej rozdíl mezi frames
                    diff = cv2.absdiff(prev_frame, gray)
                    motion_percent = (np.count_nonzero(diff > 30) / diff.size) * 100
                    
                    if motion_percent > config.QUALITY_THRESHOLDS["motion_threshold"]:
                        moving_frames += 1
                        # Pokud skončila statická část, ulož ji
                        if frame_idx - static_start > config.QUALITY_THRESHOLDS["min_motion_frames"]:
                            static_ranges.append({
                                "start_frame": static_start,
                                "end_frame": frame_idx,
                                "duration_sec": (frame_idx - static_start) / fps
                            })
                        static_start = frame_idx
                    else:
                        # Stále je to statika
                        pass
                
                prev_frame = gray
                frame_idx += 1
            
            cap.release()
            
            motion_percent = (moving_frames / max(1, frame_count)) * 100
            has_motion = motion_percent > 30  # Pokud je více než 30% pohybu, je to "dynamické"
            
            return {
                "has_motion": has_motion,
                "motion_percent": float(motion_percent),
                "static_ranges": static_ranges,
                "frame_count": frame_count
            }
        
        except Exception as e:
            return {"has_motion": False, "motion_percent": 0, "static_ranges": [], "error": str(e)}
