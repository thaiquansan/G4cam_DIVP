import cv2
import numpy as np

def adjust_saturation(frame, value):
    if value == 0:
        return frame
    
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV).astype(np.float32)
    scale = 1.0 + (value / 100.0)
    hsv[:, :, 1] = hsv[:, :, 1] * scale
    hsv[:, :, 1] = np.clip(hsv[:, :, 1], 0, 255)
    result = cv2.cvtColor(hsv.astype(np.uint8), cv2.COLOR_HSV2BGR)
    
    return result