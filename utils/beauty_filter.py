"""
Beauty filter module - SIMPLIFIED VERSION
2 modes rõ ràng và đủ dùng
"""
import cv2
import numpy as np


def apply_natural_smoothing(frame, mask, strength=0.5):
    """
    NATURAL MODE - Quick & gentle smoothing
    Best for: Real-time, subtle enhancement
    """
    if strength <= 0.0:
        return frame
    
    strength = max(0.0, min(1.0, strength))
    
    # Simple Gaussian blur
    kernel_size = int(3 + strength * 4)  # 3-7
    if kernel_size % 2 == 0:
        kernel_size += 1
    
    smoothed = cv2.GaussianBlur(frame, (kernel_size, kernel_size), 0)
    
    # Preserve edges
    kernel_sharpen = np.array([
        [0, -0.25, 0],
        [-0.25, 2, -0.25],
        [0, -0.25, 0]
    ])
    edges = cv2.filter2D(frame, -1, kernel_sharpen)
    
    alpha = strength * 0.3
    detail_preserve = 0.25 * strength
    
    blended = cv2.addWeighted(
        cv2.addWeighted(frame, 1.0 - alpha, smoothed, alpha, 0),
        1.0,
        edges,
        detail_preserve,
        0
    )
    
    soft_mask = np.clip(mask * 1.2 - 0.1, 0, 1)
    mask_3ch = np.stack([soft_mask] * 3, axis=2)
    
    result = (blended * mask_3ch + frame * (1 - mask_3ch)).astype(np.uint8)
    
    return result


def apply_smooth_beauty(frame, mask, strength=0.4):
    """
    NATURAL SKIN SMOOTHING
    - Edge locked
    - No plastic skin
    - Webcam / Zoom ready
    """
    if strength <= 0:
        return frame

    strength = np.clip(strength, 0.0, 1.0)

    try:
        f = frame.astype(np.float32) / 255.0

        # --- 1. Edge detection ---
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY).astype(np.float32) / 255.0
        gx = cv2.Sobel(gray, cv2.CV_32F, 1, 0, ksize=3)
        gy = cv2.Sobel(gray, cv2.CV_32F, 0, 1, ksize=3)
        grad = cv2.magnitude(gx, gy)

        # Edge lock mask (1 = allow smooth, 0 = protect edge)
        edge_mask = np.exp(-grad * 6.0)
        edge_mask = np.clip(edge_mask, 0, 1)

        # --- 2. Adaptive blur based on strength ---
        sigma = 0.5 + strength * 4.0   # Range: 0.5 to 4.5 (more visible effect)
        smooth = cv2.GaussianBlur(f, (0, 0), sigma)

        # --- 3. Mix using edge mask ---
        skin = f * (1 - edge_mask[..., None]) + smooth * edge_mask[..., None]

        # --- 4. Soft segmentation mask ---
        soft_mask = cv2.GaussianBlur(mask.astype(np.float32), (0, 0), 5)
        soft_mask = np.clip(soft_mask, 0, 1)

        # --- 5. Final blend with more visible alpha range ---
        alpha = 0.1 + strength * 0.5  # Range: 0.1 to 0.6 (much more responsive)
        result = f * (1 - alpha * soft_mask[..., None]) + \
                 skin * (alpha * soft_mask[..., None])

        return (np.clip(result, 0, 1) * 255).astype(np.uint8)

    except Exception as e:
        print("Smooth error:", e)
        return frame