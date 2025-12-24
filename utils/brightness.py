import cv2
import numpy as np

def adjust_brightness(frame, value):
    if value == 0:
        return frame
    
    brightness = value * 1.2
    adjusted = cv2.add(frame, np.array([brightness, brightness, brightness]))
    
    return adjusted