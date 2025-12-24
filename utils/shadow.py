import cv2
import numpy as np

def adjust_shadow(frame, value):
    if value == 0:
        return frame
    
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV).astype(np.float32)
    v = hsv[:, :, 2]
    shadow_mask = (v < 128).astype(np.float32)
    adjustment = (value / 100.0) * 50
    v += shadow_mask * adjustment
    hsv[:, :, 2] = np.clip(v, 0, 255)
    result = cv2.cvtColor(hsv.astype(np.uint8), cv2.COLOR_HSV2BGR)
    
    return result