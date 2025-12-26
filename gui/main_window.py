from PySide6 import QtCore, QtWidgets
from gui.video_widget import VideoWidget
from gui.controls_panel import ControlsPanel

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.setWindowTitle("G4Cam – GUI Only")
        
        try:
            self._build_ui()
        except Exception as e:
            print(f"❌ _build_ui failed: {e}")
            import traceback
            traceback.print_exc()
            raise
        
        try:
            self._connect_signals()
        except Exception as e:
            print(f"❌ _connect_signals failed: {e}")
            import traceback
            traceback.print_exc()
            raise
        
        try:
            self.video.set_device(0)
            self.video.set_resolution(1024, 720)            
            self.video.start_camera()
        except Exception as e:
            print(f"❌ Camera initialization failed: {e}")
            import traceback
            traceback.print_exc()

    def _build_ui(self):
        self.video = VideoWidget(self)
        self.controls = ControlsPanel(self)
        splitter = QtWidgets.QSplitter(QtCore.Qt.Horizontal, self)
        splitter.addWidget(self.video)
        splitter.addWidget(self.controls)
        splitter.setStretchFactor(0, 4)
        splitter.setStretchFactor(1, 1)
        tb = self.addToolBar("Controls")
        tb.setMovable(False)
        self.act_snapshot = tb.addAction("Snapshot")

        self.setCentralWidget(splitter)

        self.lbl_status = QtWidgets.QLabel("Starting...")
        self.statusBar().addPermanentWidget(self.lbl_status)

    def _connect_signals(self):
        self.act_snapshot.triggered.connect(self._on_snapshot)
        self.controls.sig_controls_changed.connect(self._on_controls_changed)
        self.video.sig_fps_update.connect(self._on_fps_update)

    def _on_snapshot(self):
        img = self.video.grab_current_frame()
        if img is None:
            QtWidgets.QMessageBox.information(self, "Snapshot", "No frame available.")
            return
        path, _ = QtWidgets.QFileDialog.getSaveFileName(self, "Save Snapshot", "snapshot.png", "PNG Image (*.png)")
        if path:
            from PySide6.QtGui import QPixmap
            pixmap = QPixmap.fromImage(img)
            pixmap.save(path, "PNG")
            QtWidgets.QMessageBox.information(self, "Snapshot", f"Saved to {path}")

    def _on_controls_changed(self, state_dict):
        """Cập nhật controls cho video widget"""
        self.video.set_controls(state_dict)

    def _on_fps_update(self, fps, p50_ms, p95_ms):
        self.lbl_status.setText(f"FPS: {fps:.1f} | p50: {p50_ms:.1f} ms | p95: {p95_ms:.1f} ms")