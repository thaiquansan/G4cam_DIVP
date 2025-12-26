# G4Cam_V3_San - Real-time Video Processing Application

**Course:** IVP501.22 - Image and Video Processing  
**Group 4:** Nguyễn Sỹ Hùng (25MSA33055), Nguyễn Trần Quang Mạnh (25MSA33060), Thái Quan San (25MSA33052)

## Overview

G4Cam là ứng dụng xử lý video real-time với các tính năng:
- ✨ Background segmentation và effects (blur, pixelate, color shift, virtual background)
- 🎨 Global adjustments (brightness, contrast, exposure, saturation, shadow)
- 🔧 Beauty filtering (in progress)
- 📸 Snapshot capture

## Project Structure

```
g4cam/
├── app.py                      # Entry point
├── requirements.txt            # Dependencies
│
├── gui/
│   ├── main_window.py         # Main window
│   ├── video_widget.py        # Video display widget (updated)
│   └── controls_panel.py      # Controls UI (updated)
│
├── processing/
│   ├── segmentation.py        # MediaPipe segmentation (San)
│   ├── background_processing.py  # Background effects (San)
│   ├── pipeline_processor.py  # Integrated pipeline (San)
│   └── beauty_filter.py       # Beauty filter
│
└── README.md
```

## Installation

### 1. Cài đặt Python Dependencies

```bash
pip install -r requirements.txt
```

### 2. Kiểm tra MediaPipe

MediaPipe yêu cầu:
- Python 3.8-3.11
- Webcam hoạt động
- GPU không bắt buộc nhưng sẽ tăng tốc

### 3. Chạy ứng dụng

```bash
python app.py
```

## Work Breakdown

---

### Thái Quan San - Background Processing & Pipeline Integration
**Files:** `background_processing.py`, `pipeline_processor.py`, `controls_panel.py` (updated), `video_widget.py` (updated)

**Techniques:**
- **Spatial Filters:** Gaussian blur for background
- **Morphological Operations:** Mask smoothing
- **Color Processing:** HSV color shift
- **Virtual Background:** Solid color replacement, pixelate effect

**Pipeline Formula:**
```
O_t = G(M_t ⊙ F(I_t) + (1 - M_t) ⊙ B(I_t))
```
Where:
- `I_t`: Input frame at time t
- `M_t`: Person mask from segmentation
- `F`: Foreground/beauty processing
- `B`: Background processing
- `G`: Global adjustments
- `⊙`: Element-wise multiplication

**Features Implemented:**
- ✅ Background blur với Gaussian filter
- ✅ Background pixelate (mosaic effect)
- ✅ Background color shift (HSV hue/saturation)
- ✅ Solid color virtual background
- ✅ Mask threshold và smoothing controls
- ✅ Integrated pipeline với all processing steps

**Status:** ✅ Complete

### Background Effects Panel

1. **Enable Background Effects:** Tick checkbox để bật segmentation
2. **Effect Type:** Chọn loại effect:
   - **None:** Không effect
   - **Blur:** Làm mờ nền
   - **Pixelate:** Mosaic nền
   - **Color Shift:** Thay đổi màu nền
   - **Solid Color:** Nền màu đặc
3. **Adjust Parameters:**
   - BG Blur: Độ mạnh blur (1-99)
   - BG Pixelate: Kích thước pixel (2-30)
   - BG Hue Shift: Dịch màu (0-180°)
   - BG Saturation: Độ bão hòa (50-200%)
   - Choose BG Color: Chọn màu cho solid background
4. **Segmentation Settings:**
   - Mask Threshold: Ngưỡng tách người/nền (0-100%)
   - Mask Smoothing: Làm mịn biên mask (1-15)

### Global Adjustments Panel

- **Brightness:** -100 to +100
- **Exposure:** -100 to +100 (gamma correction)
- **Contrast:** -100 to +100
- **Saturation:** -100 to +100
- **Shadow:** -100 to +100 (lift shadows)
- **Blur:** 0 to 100 (global blur)
- **Sharpen:** 0 to 100 (edge enhancement)

### Snapshot

Click "Snapshot" trong toolbar để chụp ảnh và lưu kết quả đã xử lý.

## Technical Details

### Pipeline Processing Order

1. **Segmentation** (nếu bg_enable = true)
   - MediaPipe Selfie Segmentation
   - Mask threshold và Gaussian smoothing
   
2. **Foreground Processing** (San)
   - Beauty filter on person region
   
3. **Background Processing** (San)
   - Apply effect (blur/pixelate/color shift/solid) to background
   - Combine với foreground using mask

### Performance Considerations

- **Resolution:** 1024x720 default (có thể giảm để tăng FPS)
- **Frame Rate Target:** ~30 FPS
- **Segmentation:** CPU-based, ~20-40ms per frame
- **Optimization Tips:**
  - Giảm resolution nếu FPS thấp
  - Tắt background effects khi không cần
  - Reduce mask blur size

### Known Limitations

- MediaPipe segmentation có thể chậm trên CPU yếu
- Mask có thể bị artifacts ở biên trong điều kiện ánh sáng kém
- Beauty filter chưa được implement (TODO)

## Future Enhancements

- [ ] Beauty filter implementation (San)
- [ ] Auto brightness adjustment (CLAHE)
- [ ] Virtual background with custom images
- [ ] Face mesh for detailed facial processing
- [ ] Recording functionality
- [ ] GPU acceleration

## References

- **MediaPipe:** https://google.github.io/mediapipe/
- **OpenCV:** https://opencv.org/
- **Course Materials:** IVP501.22 - Image and Video Processing

## License

Educational project - MSE-AI, FSP, 2025