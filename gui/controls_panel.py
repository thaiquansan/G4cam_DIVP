from PySide6 import QtCore, QtWidgets

class LabeledSlider(QtWidgets.QWidget):
    valueChanged = QtCore.Signal(int)
    def __init__(self, text, minimum=-100, maximum=100, value=0, parent=None):
        super().__init__(parent)
        self.label = QtWidgets.QLabel(text)
        self.slider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.slider.setRange(minimum, maximum)
        self.slider.setValue(value)
        self.val = QtWidgets.QLabel(str(value)); self.val.setFixedWidth(40)
        lay = QtWidgets.QVBoxLayout(self)
        row = QtWidgets.QHBoxLayout(); row.addWidget(self.label); row.addStretch(); row.addWidget(self.val)
        lay.addLayout(row); lay.addWidget(self.slider)
        self.slider.valueChanged.connect(self._on_value)
    def _on_value(self, v):
        self.val.setText(str(v)); self.valueChanged.emit(v)

class ControlsPanel(QtWidgets.QWidget):
    sig_controls_changed = QtCore.Signal(dict)
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumWidth(340)
        self._build_ui()

    def _build_ui(self):
        self.setStyleSheet("QGroupBox{font-weight:bold;}")

        # Master On/Off
        self.chk_onoff = QtWidgets.QCheckBox("On/Off")
        self.chk_onoff.setChecked(True)

        # Sliders: Exposure, Saturation, Contrast
        self.sld_brightness = LabeledSlider("Brightness", -100, 100, 0)
        self.sld_blur = LabeledSlider("Blur", 0, 100, 0)
        self.sld_sharpen = LabeledSlider("Sharpen", 0, 100, 0)
        self.sld_shadow = LabeledSlider("Shadow", -100, 100, 0)
        self.sld_exposure = LabeledSlider("Exposure", -100, 100, 0)
        self.sld_saturation = LabeledSlider("Saturation", -100, 100, 0)
        self.sld_contrast = LabeledSlider("Contrast", -100, 100, 0)

        lay = QtWidgets.QVBoxLayout(self)
        lay.addWidget(self.chk_onoff)

        grp_adj = QtWidgets.QGroupBox("Adjustments")
        la = QtWidgets.QVBoxLayout(grp_adj)
        la.addWidget(self.sld_brightness)
        la.addWidget(self.sld_blur)
        la.addWidget(self.sld_sharpen)
        la.addWidget(self.sld_shadow)
        la.addWidget(self.sld_exposure)
        la.addWidget(self.sld_saturation)
        la.addWidget(self.sld_contrast)

        lay.addWidget(grp_adj)
        lay.addStretch()

        # Emit state on change
        self.chk_onoff.stateChanged.connect(self._emit_state)
        slds = [self.sld_brightness, self.sld_blur, self.sld_sharpen, self.sld_shadow, self.sld_exposure, self.sld_saturation, self.sld_contrast]
        for w in slds:
            w.valueChanged.connect(lambda *_: self._emit_state())

    def _emit_state(self):
        st = dict(
            onoff=self.chk_onoff.isChecked(),
            brightness=self.sld_brightness.slider.value(),
            blur=self.sld_blur.slider.value(),
            sharpen=self.sld_sharpen.slider.value(),
            shadow=self.sld_shadow.slider.value(),
            exposure=self.sld_exposure.slider.value(),
            saturation=self.sld_saturation.slider.value(),
            contrast=self.sld_contrast.slider.value(),
        )
        self.sig_controls_changed.emit(st)
