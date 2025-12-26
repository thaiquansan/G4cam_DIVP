from PySide6 import QtCore, QtGui, QtWidgets
import cv2, time, numpy as np
from utils.pipeline_processor import IntegratedPipeline

class VideoWidget(QtWidgets.QLabel):
    sig_fps_update = QtCore.Signal(float, float, float)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumSize(640, 360)
        self.setAlignment(QtCore.Qt.AlignCenter)
        self.setStyleSheet("background:#111; color:#bbb; border:1px solid #333;")
        self._cap = None
        self._device_index = 0
        self._target_size = (1024, 720)
        self._timer = QtCore.QTimer(self)
        self._timer.timeout.connect(self._on_tick)
        self._timer.setInterval(30)
        self._times = []

        self._controls = {}
        self._current_frame = None
        
        # Khởi tạo integrated pipeline
        self.pipeline = IntegratedPipeline()

    def start_camera(self):
        self.stop_camera()
        self._cap = cv2.VideoCapture(self._device_index, cv2.CAP_ANY)
        w,h = self._target_size
        self._cap.set(cv2.CAP_PROP_FRAME_WIDTH, w)
        self._cap.set(cv2.CAP_PROP_FRAME_HEIGHT, h)
        if not self._cap.isOpened():
            self.setText("Failed to open camera")
            return
        self._times.clear()
        self._timer.start()

    def stop_camera(self):
        self._timer.stop()
        if self._cap is not None:
            self._cap.release()
            self._cap = None
        self.setText("Camera stopped")

    def set_device(self, index:int):
        self._device_index = index

    def set_resolution(self, w:int, h:int):
        self._target_size = (w,h)
        
    def set_controls(self, controls_dict):
        """Cập nhật trạng thái controls"""
        self._controls = controls_dict

    def _on_tick(self):
        if self._cap is None:
            return
        t0 = time.perf_counter()
        ok, frame = self._cap.read()
        if not ok:
            self.setText("No frame")
            return
        
        # Lật cam
        frame = cv2.flip(frame, 1)
        
        # === Áp dụng INTEGRATED PIPELINE ===
        if self._controls:
            frame = self.pipeline.process(frame, self._controls)
        
        # Lưu frame đã xử lý
        self._current_frame = frame.copy()

        # Hiển thị
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        h, w, ch = frame_rgb.shape
        qimg = QtGui.QImage(frame_rgb.data, w, h, ch*w, QtGui.QImage.Format.Format_RGB888)
        pix = QtGui.QPixmap.fromImage(qimg).scaled(self.size(), QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)
        self.setPixmap(pix)

        # Tính FPS
        dt = (time.perf_counter() - t0) * 1000.0
        self._times.append(dt)
        if len(self._times) > 60:
            self._times.pop(0)
        if self._times:
            p50 = float(np.percentile(self._times, 50))
            p95 = float(np.percentile(self._times, 95))
            avg = float(np.mean(self._times))
            fps = 1000.0/avg if avg>1e-3 else 0.0
            self.sig_fps_update.emit(fps, p50, p95)

    def grab_current_frame(self):
        """Lấy frame hiện tại đã xử lý"""
        if self._current_frame is not None:
            # Chuyển BGR sang RGB cho QImage
            frame_rgb = cv2.cvtColor(self._current_frame, cv2.COLOR_BGR2RGB)
            h, w, ch = frame_rgb.shape
            qimg = QtGui.QImage(frame_rgb.data, w, h, ch*w, QtGui.QImage.Format.Format_RGB888)
            return qimg.copy()
        return None
    
    def cleanup(self):
        """Giải phóng tài nguyên khi đóng app"""
        self.stop_camera()
        self.pipeline.cleanup()