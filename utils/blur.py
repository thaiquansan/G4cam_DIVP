import cv2

def apply_blur(frame, value):
    if value <= 0:
        return frame
    
    kernel_size = int((value / 100.0) * 24) * 2 + 3
    kernel_size = max(3, min(kernel_size, 51))
    blurred = cv2.GaussianBlur(frame, (kernel_size, kernel_size), 0)
    
    return blurred