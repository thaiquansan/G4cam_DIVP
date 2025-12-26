import cv2
import numpy as np

# =========================
# Background-only processing
# =========================

def blur_background(frame, blur_strength=15):
    if blur_strength <= 0:
        return frame

    k = blur_strength if blur_strength % 2 == 1 else blur_strength + 1
    k = max(3, min(k, 99))
    return cv2.GaussianBlur(frame, (k, k), 0)


def pixelate_background(frame, pixel_size=10):
    if pixel_size <= 1:
        return frame

    h, w = frame.shape[:2]
    small = cv2.resize(frame, (w // pixel_size, h // pixel_size),
                       interpolation=cv2.INTER_LINEAR)
    return cv2.resize(small, (w, h), interpolation=cv2.INTER_NEAREST)


def color_shift_background(frame, hue_shift=30, saturation_scale=1.5):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV).astype(np.float32)

    hsv[:, :, 0] = (hsv[:, :, 0] + hue_shift) % 180
    hsv[:, :, 1] = np.clip(hsv[:, :, 1] * saturation_scale, 0, 255)

    return cv2.cvtColor(hsv.astype(np.uint8), cv2.COLOR_HSV2BGR)


def solid_color_background(frame, bg_color=(0, 255, 0)):
    return np.full_like(frame, bg_color, dtype=np.uint8)
