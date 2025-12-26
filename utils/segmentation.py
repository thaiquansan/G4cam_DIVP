"""
Module segmentation using MediaPipe Selfie Segmentation
Fixed to handle MediaPipe API correctly
"""
import cv2
import numpy as np
import mediapipe as mp
import os
from pathlib import Path

class PersonSegmenter:
    def __init__(self, model_selection=1):
        """
        Initialize PersonSegmenter with automatic model handling
        
        Args:
            model_selection: 0 for general model (256x256), 1 for landscape model (256x144)
        """
        # Try to find model file in multiple locations
        possible_paths = [
            Path(__file__).parent.parent / "selfie_segmenter.tflite",
            Path(__file__).parent.parent / "selfie_segmentation.tflite",
            Path.cwd() / "selfie_segmenter.tflite",
            Path.cwd() / "selfie_segmentation.tflite",
            Path.cwd() / "models" / "selfie_segmenter.tflite",
            Path.cwd() / "models" / "selfie_segmentation.tflite",
        ]
        
        model_path = None
        for path in possible_paths:
            if path.exists():
                model_path = str(path)
                break
        
        if model_path is None:
            print("⚠️ Model file not found. Attempting to use MediaPipe's built-in model...")
            self._init_with_builtin_model(model_selection)
        else:
            self._init_with_file_model(model_path)
        
        self._enabled = True

    def _init_with_file_model(self, model_path):
        """Initialize with local model file"""
        try:
            BaseOptions = mp.tasks.BaseOptions
            VisionRunningMode = mp.tasks.vision.RunningMode
            ImageSegmenter = mp.tasks.vision.ImageSegmenter
            ImageSegmenterOptions = mp.tasks.vision.ImageSegmenterOptions

            options = ImageSegmenterOptions(
                base_options=BaseOptions(model_asset_path=model_path),
                running_mode=VisionRunningMode.IMAGE,
                output_category_mask=True,
                output_confidence_masks=False  # We only need category mask
            )
            self.segmenter = ImageSegmenter.create_from_options(options)
            self.use_legacy = False
        except Exception as e:
            print(f"❌ Failed to create segmenter with local model: {e}")
            import traceback
            traceback.print_exc()
            raise

    def _init_with_builtin_model(self, model_selection):
        """Initialize with MediaPipe's selfie segmentation solution (fallback)"""
        try:
            # Fallback to legacy selfie segmentation
            self.mp_selfie_segmentation = mp.solutions.selfie_segmentation
            self.segmenter = self.mp_selfie_segmentation.SelfieSegmentation(
                model_selection=model_selection
            )
            self.use_legacy = True
        except Exception as e:
            print(f"❌ Failed to initialize segmentation: {e}")
            raise

    def set_enabled(self, enabled: bool):
        """Enable/disable segmentation"""
        self._enabled = enabled

    def is_enabled(self):
        """Check if segmentation is enabled"""
        return self._enabled

    def get_mask(self, frame):
        """
        Get raw mask from MediaPipe
        
        Args:
            frame: numpy array (BGR format)
            
        Returns:
            numpy array with values 0 (background) or 1 (person)
        """
        if not self._enabled:
            return np.ones((frame.shape[0], frame.shape[1]), dtype=np.float32)

        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        try:
            if hasattr(self, 'use_legacy') and self.use_legacy:
                # Legacy API
                results = self.segmenter.process(frame_rgb)
                if results.segmentation_mask is None:
                    print("⚠️ Legacy segmentation returned None")
                    return np.ones((frame.shape[0], frame.shape[1]), dtype=np.float32)
                mask = results.segmentation_mask
            else:
                # New API
                mp_image = mp.Image(
                    image_format=mp.ImageFormat.SRGB,
                    data=frame_rgb
                )
                result = self.segmenter.segment(mp_image)
                
                # Check if result is None or doesn't have category_mask
                if result is None:
                    print("⚠️ Segmentation returned None")
                    return np.ones((frame.shape[0], frame.shape[1]), dtype=np.float32)
                
                if not hasattr(result, 'category_mask') or result.category_mask is None:
                    print("⚠️ No category_mask in result")
                    return np.ones((frame.shape[0], frame.shape[1]), dtype=np.float32)
                
                # Get the mask array
                mask = result.category_mask.numpy_view()
            
            # Ensure mask is valid
            if mask is None:
                print("⚠️ Mask is None after extraction")
                return np.ones((frame.shape[0], frame.shape[1]), dtype=np.float32)
            
            return mask
            
        except Exception as e:
            print(f"⚠️ Segmentation error: {e}")
            import traceback
            traceback.print_exc()
            return np.ones((frame.shape[0], frame.shape[1]), dtype=np.float32)

    def get_refined_mask(self, frame, threshold=0.5, blur_size=5):
        """
        Get refined mask with smoothing and morphological operations
        
        Args:
            frame: numpy array (BGR format)
            threshold: float (0-1) - threshold for person/background classification
            blur_size: int - kernel size for mask smoothing
            
        Returns:
            numpy array (H, W) with continuous values [0, 1] (float32)
        """
        try:
            # Get raw mask
            raw_mask = self.get_mask(frame)
            
            # If get_mask returned a fallback (all ones), return it
            if raw_mask is None:
                return np.ones((frame.shape[0], frame.shape[1]), dtype=np.float32)
            
            # Convert to float32 if needed
            if raw_mask.dtype != np.float32:
                mask = raw_mask.astype(np.float32)
            else:
                mask = raw_mask.copy()
            
            # Normalize to [0, 1] if needed
            if mask.max() > 1.0:
                mask = mask / 255.0
            
            # Apply threshold
            mask = 1.0 - (mask > threshold).astype(np.float32)
            
            # Morphological operations to smooth edges
            kernel = np.ones((3, 3), np.uint8)
            mask_uint8 = (mask * 255).astype(np.uint8)
            
            # Closing: remove small holes
            mask_uint8 = cv2.morphologyEx(mask_uint8, cv2.MORPH_CLOSE, kernel, iterations=1)
            
            # Opening: remove noise
            mask_uint8 = cv2.morphologyEx(mask_uint8, cv2.MORPH_OPEN, kernel, iterations=1)
            
            # Convert back to float
            mask = mask_uint8.astype(np.float32) / 255.0
            
            # Smooth edges with Gaussian blur
            if blur_size > 0:
                # Ensure blur_size is odd
                blur_size = blur_size if blur_size % 2 == 1 else blur_size + 1
                blur_size = max(3, min(blur_size, 15))  # Limit 3-15
                mask = cv2.GaussianBlur(mask, (blur_size, blur_size), 0)
            
            return mask
            
        except Exception as e:
            print(f"⚠️ Error in get_refined_mask: {e}")
            import traceback
            traceback.print_exc()
            return np.ones((frame.shape[0], frame.shape[1]), dtype=np.float32)

    def close(self):
        """Clean up resources"""
        try:
            if hasattr(self, 'segmenter'):
                self.segmenter.close()
        except Exception as e:
            print(f"⚠️ Error closing segmenter: {e}")