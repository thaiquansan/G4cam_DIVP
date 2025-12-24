import cv2
import numpy as np

def apply_sharpen(frame, value):
    if value <= 0:
        return frame
    
    strength = (value / 100.0) * 2.0
    kernel = np.array([
        [0, -1, 0],
        [-1, 4, -1],
        [0, -1, 0]
    ], dtype=np.float32)
    kernel = (kernel - 1) * strength + 1
    kernel[1, 1] = 1 + 4 * strength
    sharpened = cv2.filter2D(frame, -1, kernel)
    
    return sharpened