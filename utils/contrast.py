import cv2
import numpy as np

def adjust_contrast(frame, value):
    if value == 0:
        return frame
    
    factor = 1.0 + (value / 100.0) * 1.5
    adjusted = cv2.convertScaleAbs(frame, alpha=factor, beta=127.5 * (1 - factor))
    return adjusted