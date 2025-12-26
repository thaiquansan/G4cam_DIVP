from PySide6 import QtCore, QtWidgets

class LabeledSlider(QtWidgets.QWidget):
    valueChanged = QtCore.Signal(int)
    def __init__(self, text, minimum=-100, maximum=100, value=0, parent=None):
        super().__init__(parent)
        self.label = QtWidgets.QLabel(text)
        self.slider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.slider.setRange(minimum, maximum)
        self.slider.setValue(value)
        self.val = QtWidgets.QLabel(str(value))
        self.val.setFixedWidth(40)
        self.val.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        
        lay = QtWidgets.QVBoxLayout(self)
        lay.setContentsMargins(0, 0, 0, 0)
        row = QtWidgets.QHBoxLayout()
        row.addWidget(self.label)
        row.addStretch()
        row.addWidget(self.val)
        lay.addLayout(row)
        lay.addWidget(self.slider)
        self.slider.valueChanged.connect(self._on_value)
        
    def _on_value(self, v):
        self.val.setText(str(v))
        self.valueChanged.emit(v)

class ControlsPanel(QtWidgets.QWidget):
    sig_controls_changed = QtCore.Signal(dict)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumWidth(340)
        self.setMaximumWidth(400)
        self._build_ui()

    def _build_ui(self):
        # Main layout
        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.setContentsMargins(5, 5, 5, 5)
        
        # Create scroll area
        scroll = QtWidgets.QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        scroll.setFrameShape(QtWidgets.QFrame.NoFrame)
        
        # Container widget for scroll content
        container = QtWidgets.QWidget()
        scroll.setWidget(container)
        
        # Layout for scrollable content
        layout = QtWidgets.QVBoxLayout(container)
        layout.setSpacing(10)
        
        # Styling
        self.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                border: 1px solid #444;
                border-radius: 5px;
                margin-top: 10px;
                padding-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px;
            }
        """)

        # === MASTER ON/OFF ===
        self.chk_onoff = QtWidgets.QCheckBox("Enable All Effects")
        self.chk_onoff.setChecked(True)
        self.chk_onoff.setStyleSheet("font-weight: bold; font-size: 12pt;")
        layout.addWidget(self.chk_onoff)
        
        # === 1. SEGMENTATION SETTINGS ===
        grp_seg = QtWidgets.QGroupBox("1️⃣ Segmentation Settings")
        lay_seg = QtWidgets.QVBoxLayout(grp_seg)
        
        self.chk_seg_enable = QtWidgets.QCheckBox("Enable Segmentation")
        self.chk_seg_enable.setChecked(False)
        self.chk_seg_enable.setToolTip("Enable person/background separation")
        
        self.sld_mask_threshold = LabeledSlider("Mask Threshold", 0, 100, 50)
        self.sld_mask_threshold.setToolTip("Adjust person detection sensitivity")
        
        self.sld_mask_blur = LabeledSlider("Mask Smoothing", 1, 15, 5)
        self.sld_mask_blur.setToolTip("Smooth mask edges")
        
        lay_seg.addWidget(self.chk_seg_enable)
        lay_seg.addWidget(self.sld_mask_threshold)
        lay_seg.addWidget(self.sld_mask_blur)
        
        layout.addWidget(grp_seg)

        # === 2. BEAUTY FILTER ===
        grp_beauty = QtWidgets.QGroupBox("2️⃣ Beauty Filter (Foreground)")
        lay_beauty = QtWidgets.QVBoxLayout(grp_beauty)
        
        self.chk_beauty_enable = QtWidgets.QCheckBox("Enable Beauty Filter")
        self.chk_beauty_enable.setChecked(False)
        self.chk_beauty_enable.setToolTip("Apply skin smoothing to person")
        
        self.sld_beauty_strength = LabeledSlider("Smoothing Strength", 0, 100, 50)
        self.sld_beauty_strength.setToolTip("Skin smoothing intensity (0-100)")
        
        # Beauty mode selector
        lay_beauty.addWidget(QtWidgets.QLabel("Filter Mode:"))
        self.cmb_beauty_mode = QtWidgets.QComboBox()
        self.cmb_beauty_mode.addItems(["Natural", "Smooth"])
        self.cmb_beauty_mode.setToolTip("Natural: Fast & light | Smooth: Professional skin smoothing")
        
        lay_beauty.addWidget(self.chk_beauty_enable)
        lay_beauty.addWidget(self.sld_beauty_strength)
        lay_beauty.addWidget(self.cmb_beauty_mode)
        
        # Info label
        info_label = QtWidgets.QLabel("ℹ️ Gentle smoothing with detail preservation")
        info_label.setWordWrap(True)
        info_label.setStyleSheet("color: #888; font-size: 9pt;")
        lay_beauty.addWidget(info_label)
        
        layout.addWidget(grp_beauty)

        # === 3. BACKGROUND EFFECTS ===
        grp_bg = QtWidgets.QGroupBox("3️⃣ Background Effects")
        lay_bg = QtWidgets.QVBoxLayout(grp_bg)
        
        self.chk_bg_enable = QtWidgets.QCheckBox("Enable Background Effects")
        self.chk_bg_enable.setChecked(False)
        self.chk_bg_enable.setToolTip("Apply effects to background only")
        
        lay_bg.addWidget(self.chk_bg_enable)
        
        # Effect type selector
        lay_bg.addWidget(QtWidgets.QLabel("Effect Type:"))
        self.cmb_bg_effect = QtWidgets.QComboBox()
        self.cmb_bg_effect.addItems(["None", "Blur", "Pixelate", "Color Shift", "Solid Color"])
        lay_bg.addWidget(self.cmb_bg_effect)
        
        # Effect parameters
        self.sld_bg_blur = LabeledSlider("Blur Strength", 1, 99, 15)
        self.sld_bg_pixelate = LabeledSlider("Pixel Size", 2, 30, 10)
        self.sld_bg_hue = LabeledSlider("Hue Shift", 0, 180, 30)
        self.sld_bg_sat = LabeledSlider("Saturation", 50, 200, 150)
        
        lay_bg.addWidget(self.sld_bg_blur)
        lay_bg.addWidget(self.sld_bg_pixelate)
        lay_bg.addWidget(self.sld_bg_hue)
        lay_bg.addWidget(self.sld_bg_sat)
        
        # Color picker for solid background
        color_row = QtWidgets.QHBoxLayout()
        self.btn_bg_color = QtWidgets.QPushButton("Choose Color")
        self.lbl_bg_color = QtWidgets.QLabel()
        self.lbl_bg_color.setFixedSize(40, 20)
        self.lbl_bg_color.setStyleSheet("background-color: rgb(0, 255, 0); border: 1px solid #999;")
        self._bg_color = (0, 255, 0)  # BGR format
        color_row.addWidget(self.btn_bg_color)
        color_row.addWidget(self.lbl_bg_color)
        color_row.addStretch()
        lay_bg.addLayout(color_row)
        
        layout.addWidget(grp_bg)
        
        # Add stretch at the end to push everything to top
        layout.addStretch()

        # Add scroll area to main layout
        main_layout.addWidget(scroll)
        
        # === CONNECT SIGNALS ===
        self.chk_onoff.stateChanged.connect(self._emit_state)
        self.chk_seg_enable.stateChanged.connect(self._emit_state)
        self.chk_beauty_enable.stateChanged.connect(self._emit_state)
        self.cmb_beauty_mode.currentIndexChanged.connect(self._emit_state)
        self.chk_bg_enable.stateChanged.connect(self._emit_state)
        self.cmb_bg_effect.currentIndexChanged.connect(self._emit_state)
        self.btn_bg_color.clicked.connect(self._choose_bg_color)
        
        # Connect all sliders
        sliders = [
            self.sld_mask_threshold, self.sld_mask_blur,
            self.sld_beauty_strength,
            self.sld_bg_blur, self.sld_bg_pixelate, self.sld_bg_hue, self.sld_bg_sat,
        ]
        for slider in sliders:
            slider.valueChanged.connect(lambda *_: self._emit_state())

    def _choose_bg_color(self):
        from PySide6.QtWidgets import QColorDialog
        from PySide6.QtGui import QColor
        
        # Convert BGR to RGB for QColor
        r, g, b = self._bg_color[2], self._bg_color[1], self._bg_color[0]
        initial = QColor(r, g, b)
        
        color = QColorDialog.getColor(initial, self, "Choose Background Color")
        if color.isValid():
            # Convert RGB to BGR
            self._bg_color = (color.blue(), color.green(), color.red())
            self.lbl_bg_color.setStyleSheet(
                f"background-color: rgb({color.red()}, {color.green()}, {color.blue()}); border: 1px solid #999;"
            )
            self._emit_state()

    def _emit_state(self):
        """Emit current state of all controls"""
        state = {
            # Master switch
            'onoff': self.chk_onoff.isChecked(),
            
            # Segmentation settings
            'seg_enable': self.chk_seg_enable.isChecked(),
            'mask_threshold': self.sld_mask_threshold.slider.value() / 100.0,
            'mask_blur_size': self.sld_mask_blur.slider.value(),
            
            # Beauty filter
            'beauty_enable': self.chk_beauty_enable.isChecked(),
            'beauty_strength': self.sld_beauty_strength.slider.value() / 100.0,
            'beauty_mode': self.cmb_beauty_mode.currentText(),
            
            # Background effects
            'bg_enable': self.chk_bg_enable.isChecked(),
            'bg_effect': self.cmb_bg_effect.currentText(),
            'bg_blur_strength': self.sld_bg_blur.slider.value(),
            'bg_pixelate_size': self.sld_bg_pixelate.slider.value(),
            'bg_hue_shift': self.sld_bg_hue.slider.value(),
            'bg_saturation_scale': self.sld_bg_sat.slider.value() / 100.0,
            'bg_color': self._bg_color,
        }
        self.sig_controls_changed.emit(state)