import time
import cv2
import numpy as np
import mss
import ctypes
import math
from ultralytics import YOLO
import pyautogui
pyautogui.PAUSE = 0.0
pyautogui.FAILSAFE = False

def get_dpi_scaling():
    #获取系统DPI比例
    try:
        user32 = ctypes.windll.user32
        hwnd = user32.GetDesktopWindow()
        dc = user32.GetDC(hwnd)
        dpi = ctypes.windll.gdi32.GetDeviceCaps(dc, 88)
        user32.ReleaseDC(hwnd, dc)
        return dpi / 96.0
    except Exception:
        return 1.0
class MinecraftZombieDetector:
    def __init__(self, model_path: str, monitor_index: int = 1, conf_threshold: float = 0.5, 
                    aim_smooth: float = 1.0, head_offset_ratio: float = 0.15, 
                    game_sensitivity: float = 1.2):
     
        self.model = YOLO(model_path)
        self.conf_threshold = conf_threshold
        self.sct = mss.mss()
        self.aim_smooth = aim_smooth
        self.head_offset_ratio = head_offset_ratio
        self.game_sensitivity = game_sensitivity
        self.dpi_scale = get_dpi_scaling()
        monitor = self.sct.monitors[monitor_index]
        self.left = monitor["left"]
        self.top = monitor["top"]
        self.width = monitor["width"]
        self.height = monitor["height"]
        self.center_x = self.width / 2
        self.center_y = self.height / 2
        self.fps = 0.0
        self.avg_confidence = 0.0
     
        self.error_x = 0.0
        self.error_y = 0.0
    def capture_screen(self) -> np.ndarray:
        monitor = {"left": self.left, "top": self.top, "width": self.width, "height": self.height}
        img = np.array(self.sct.grab(monitor))
        return cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
    def process_and_control(self, frame: np.ndarray):
        start_time = time.perf_counter()
        
        results = self.model(frame, imgsz=640, conf=self.conf_threshold, verbose=False)
        inference_time = time.perf_counter() - start_time
        self.fps = 1.0 / inference_time if inference_time > 0 else 0
        cx, cy = int(self.center_x), int(self.center_y)
        cv2.line(frame, (cx - 15, cy), (cx + 15, cy), (0, 0, 255), 2)
        cv2.line(frame, (cx, cy - 15), (cx, cy + 15), (0, 0, 255), 2)
        boxes = results[0].boxes
        if len(boxes) > 0:
            status_text = "Status: Target Detected"
            status_color = (0, 255, 0) 
            confidences = boxes.conf.cpu().numpy()
            self.avg_confidence = float(np.mean(confidences))
            highest_conf_idx = np.argmax(confidences)
            best_box_xyxy = boxes.xyxy[highest_conf_idx].cpu().numpy()
            x_min, y_min, x_max, y_max = best_box_xyxy
            box_w = x_max - x_min
            box_h = y_max - y_min
            
            target_x = (x_min + x_max) / 2 + box_w * 0.05
            target_y = (y_min + y_max) / 2
            
            target_y -= box_h * self.head_offset_ratio
            dx = target_x - self.center_x
            dy = target_y - self.center_y
            
            dx_logical = dx / self.dpi_scale / self.game_sensitivity
            dy_logical = dy / self.dpi_scale / self.game_sensitivity
           
            raw_move_x = dx_logical * self.aim_smooth + self.error_x
            raw_move_y = dy_logical * self.aim_smooth + self.error_y
            
            max_move = 80  
            raw_move_x = max(-max_move, min(max_move, raw_move_x))
            raw_move_y = max(-max_move, min(max_move, raw_move_y))
            
            move_x = math.floor(raw_move_x)
            move_y = math.floor(raw_move_y)
            
            self.error_x = raw_move_x - move_x
            self.error_y = raw_move_y - move_y
            
            if abs(dx) > 5 and abs(move_x) < 1:
                move_x = 1 if dx > 0 else -1
            if abs(dy) > 5 and abs(move_y) < 1:
                move_y = 1 if dy > 0 else -1
            ctypes.windll.user32.mouse_event(0x0001, move_x, move_y, 0, 0)
            
            cv2.circle(frame, (int(target_x), int(target_y)), 5, (0, 255, 255), -1)
            cv2.rectangle(frame, (int(x_min), int(y_min)), (int(x_max), int(y_max)), (0, 255, 0), 2)
            cv2.line(frame, (cx, cy), (int(target_x), int(target_y)), (0, 255, 0), 1)
        else:
            status_text = "Status: Searching..."
            status_color = (0, 0, 255) 
            self.avg_confidence = 0.0
            
            self.error_x = 0.0
            self.error_y = 0.0
        # UI
        cv2.putText(frame, f"FPS: {self.fps:.2f}", (30, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv2.putText(frame, f"Conf: {self.avg_confidence:.2f}", (30, 90), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv2.putText(frame, status_text, (30, 130), cv2.FONT_HERSHEY_SIMPLEX, 1, status_color, 2)
        return frame
    def run(self):
        print(f"系统DPI缩放比例: {self.dpi_scale}")
        print("开始实时视角控制")
        try:
            while True:
                frame = self.capture_screen()
                processed_frame = self.process_and_control(frame)
                
                resized_frame = cv2.resize(processed_frame, (960, 540))
                cv2.imshow("Minecraft Zombie Detector", resized_frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
        except KeyboardInterrupt:
            pass
        finally:
            cv2.destroyAllWindows()
            self.sct.close()
            print("检测已停止。")
if __name__ == "__main__":
    MODEL_PATH = r"..\best.pt"
    detector = MinecraftZombieDetector(
        model_path=MODEL_PATH, 
        conf_threshold=0.6, 
        aim_smooth=5.0,          
        head_offset_ratio=0.15,   
        game_sensitivity=1.2     
    )
    detector.run()
