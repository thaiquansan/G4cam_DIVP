import numpy as np
import cv2
from utils.segmentation import PersonSegmenter
from utils.background_processing import (
    blur_background,
    pixelate_background,
    color_shift_background,
    solid_color_background
)
from utils.beauty_filter import apply_natural_smoothing, apply_smooth_beauty


class IntegratedPipeline:
    """
    O_t = G(M ⊙ F(I) + (1 - M) ⊙ B(I))
    
    Where:
    - I: Input frame
    - M: Person mask from segmentation
    - F: Foreground processing (beauty filter)
    - B: Background processing (blur, pixelate, etc.)
    - G: Global adjustments (removed - handled separately)
    """

    def __init__(self):
        self.segmenter = None

    def _ensure_segmenter(self):
        if self.segmenter is None:
            self.segmenter = PersonSegmenter(model_selection=1)
        return True
    
    def _needs_background_processing(self, controls):
        """Check if background effect is actually needed"""
        if not controls.get('bg_enable', False):
            return False
        effect = controls.get('bg_effect', 'None')
        return effect != 'None'

    def _apply_beauty_filter(self, frame, mask, controls):
        """
        Apply beauty filter to foreground (person) region
        
        Args:
            frame: Input frame (BGR)
            mask: Person mask [0, 1]
            controls: Control parameters
            
        Returns:
            Frame with beauty filter applied to person region
        """
        if not controls.get('beauty_enable', False):
            return frame
        
        strength = controls.get('beauty_strength', 0.5)
        mode = controls.get('beauty_mode', 'Natural')
        
        if mode == 'Natural':
            return apply_natural_smoothing(frame, mask, strength)
        elif mode == 'Smooth':
            return apply_smooth_beauty(frame, mask, strength)
        else:
            return frame

    def process(self, frame, controls):
        """
        Process frame through the integrated pipeline
        
        Pipeline order:
        1. Segmentation (if enabled)
        2. Beauty filter on foreground
        3. Background effects
        4. Composite foreground + background
        
        Args:
            frame: Input frame (BGR)
            controls: Dictionary of control parameters
            
        Returns:
            Processed frame
        """
        if not controls.get('onoff', True):
            return frame

        I_t = frame.copy()
        M_t = None

        # === SEGMENTATION ===
        # Enable segmentation if either beauty filter or background effects are on
        need_segmentation = (
            controls.get('seg_enable', False) or 
            controls.get('beauty_enable', False) or 
            self._needs_background_processing(controls)
        )
        
        if need_segmentation:
            self._ensure_segmenter()
            M_t = self.segmenter.get_refined_mask(
                I_t,
                threshold=controls.get('mask_threshold', 0.5),
                blur_size=controls.get('mask_blur_size', 5)
            )

        # If no mask → return original frame (no processing needed)
        if M_t is None:
            return I_t

        # === FOREGROUND PROCESSING (Beauty Filter) ===
        F_I = self._apply_beauty_filter(I_t, M_t, controls)

        # === BACKGROUND PROCESSING ===
        B_I = I_t
        if controls.get('bg_enable', False):
            effect = controls.get('bg_effect', 'None')

            if effect == 'Blur':
                B_I = blur_background(I_t, controls.get('bg_blur_strength', 15))

            elif effect == 'Pixelate':
                B_I = pixelate_background(I_t, controls.get('bg_pixelate_size', 10))

            elif effect == 'Color Shift':
                B_I = color_shift_background(
                    I_t,
                    controls.get('bg_hue_shift', 30),
                    controls.get('bg_saturation_scale', 1.5)
                )

            elif effect == 'Solid Color':
                B_I = solid_color_background(
                    I_t,
                    controls.get('bg_color', (0, 255, 0))
                )

        # === COMPOSITE: M ⊙ F(I) + (1 - M) ⊙ B(I) ===
        # Use soft threshold for smooth blending
        compose_mask = cv2.GaussianBlur(M_t.astype(np.float32), (0, 0), 5)
        compose_mask = np.clip(compose_mask, 0, 1)
        M_3ch = np.stack([compose_mask] * 3, axis=2)

        result = (F_I * M_3ch + B_I * (1 - M_3ch)).astype(np.uint8)

        return result

    def cleanup(self):
        """Clean up resources"""
        if self.segmenter is not None:
            self.segmenter.close()