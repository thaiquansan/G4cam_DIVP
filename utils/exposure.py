import cv2
import numpy as np

def adjust_exposure(frame, value):
    if value == 0:
        return frame
    
    if value < 0:
        gamma = 1.0 - (abs(value) / 100.0) * 0.5
    else:
        gamma = 1.0 + (value / 100.0) * 1.5
    
    inv_gamma = 1.0 / gamma
    table = np.array([
        ((i / 255.0) ** inv_gamma) * 255 
        for i in range(256)
    ]).astype(np.uint8)
    adjusted = cv2.LUT(frame, table)
    
    return adjusted