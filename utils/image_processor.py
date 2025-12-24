"""
Module tổng hợp xử lý ảnh
"""
from .brightness import adjust_brightness
from .blur import apply_blur
from .sharpen import apply_sharpen
from .shadow import adjust_shadow
from .exposure import adjust_exposure
from .saturation import adjust_saturation
from .contrast import adjust_contrast


def process_frame(frame, controls):
    """
    Xử lý frame với tất cả các điều chỉnh từ controls
    
    Args:
        frame: numpy array (BGR format)
        controls: dict chứa các giá trị điều chỉnh
            {
                'onoff': bool,
                'brightness': int,
                'blur': int,
                'sharpen': int,
                'shadow': int,
                'exposure': int,
                'saturation': int,
                'contrast': int
            }
    
    Returns:
        numpy array đã được xử lý
    """
    # Nếu tắt, trả về frame gốc
    if not controls.get('onoff', True):
        return frame
    
    result = frame.copy()
    
    # Áp dụng các điều chỉnh theo thứ tự hợp lý
    # 1. Exposure (ảnh hưởng tổng thể đến độ sáng)
    if controls.get('exposure', 0) != 0:
        result = adjust_exposure(result, controls['exposure'])
    
    # 2. Brightness (điều chỉnh độ sáng tuyến tính)
    if controls.get('brightness', 0) != 0:
        result = adjust_brightness(result, controls['brightness'])
    
    # 3. Shadow (điều chỉnh vùng tối)
    if controls.get('shadow', 0) != 0:
        result = adjust_shadow(result, controls['shadow'])
    
    # 4. Contrast (tăng/giảm sự khác biệt giữa sáng/tối)
    if controls.get('contrast', 0) != 0:
        result = adjust_contrast(result, controls['contrast'])
    
    # 5. Saturation (điều chỉnh độ bão hòa màu)
    if controls.get('saturation', 0) != 0:
        result = adjust_saturation(result, controls['saturation'])
    
    # 6. Blur (làm mờ - áp dụng trước sharpen)
    if controls.get('blur', 0) > 0:
        result = apply_blur(result, controls['blur'])
    
    # 7. Sharpen (làm sắc nét - áp dụng cuối)
    if controls.get('sharpen', 0) > 0:
        result = apply_sharpen(result, controls['sharpen'])
    
    return result