from PySide6.QtCore import Signal
from PySide6.QtWidgets import QSlider, QSpinBox, QWidget

from tacty.ui.models.project import TrackingOptions

from .tracking_ui import Ui_Form


class TrackingForm(QWidget):
    ui: Ui_Form
    data: TrackingOptions
    trackingData: bool

    startProcessing: Signal = Signal()
    resetTrackingData: Signal = Signal()

    def __init__(self, data: TrackingOptions, trackingData: bool):
        super().__init__()

        # load the ui
        self.ui = Ui_Form()
        _ = self.ui.setupUi(self)  # pyright: ignore [reportUnknownMemberType]

        # update the data
        self.trackingData = trackingData
        self.data = data

        # connectors
        _ = self.ui.track.clicked.connect(self.startProcessing.emit)
        _ = self.ui.reset.clicked.connect(self.resetTrackingData.emit)

        tolerance_pairs = [
            ("r", self.ui.redTolerance, self.ui.redToleranceSlider),
            ("y", self.ui.yellowTolerance, self.ui.yellowToleranceSlider),
            ("g", self.ui.greenTolerance, self.ui.greenToleranceSlider),
            ("c", self.ui.cyanTolerance, self.ui.cyanToleranceSlider),
            ("b", self.ui.blueTolerance, self.ui.blueToleranceSlider),
            ("m", self.ui.magentaTolerance, self.ui.magentaToleranceSlider),
        ]

        for color, spin, slider in tolerance_pairs:
            # Use default arguments (a=attr, s=spin, t=slider) to capture
            # the current values in the loop for the lambda closure
            _ = spin.valueChanged.connect(
                lambda _, a=color, s=spin, t=slider: self.syncTolerance(a, s, t)  # pyright: ignore [reportUnknownArgumentType, reportUnknownLambdaType]
            )
            _ = slider.valueChanged.connect(
                lambda _, a=color, s=slider, t=spin: self.syncTolerance(a, s, t)  # pyright: ignore [reportUnknownArgumentType, reportUnknownLambdaType]
            )

        self.updateData()

    def updateData(self):
        # hues
        self.ui.redHue.setValue(self.data.hues.r)
        self.ui.yellowHue.setValue(self.data.hues.y)
        self.ui.greenHue.setValue(self.data.hues.g)
        self.ui.cyanHue.setValue(self.data.hues.c)
        self.ui.blueHue.setValue(self.data.hues.b)
        self.ui.magentaHue.setValue(self.data.hues.m)

        # tolerances
        self.ui.redTolerance.setValue(int(self.data.tolerances.r * 100))
        self.ui.yellowTolerance.setValue(int(self.data.tolerances.y * 100))
        self.ui.greenTolerance.setValue(int(self.data.tolerances.g * 100))
        self.ui.cyanTolerance.setValue(int(self.data.tolerances.c * 100))
        self.ui.blueTolerance.setValue(int(self.data.tolerances.b * 100))
        self.ui.magentaTolerance.setValue(int(self.data.tolerances.m * 100))

        # buttons
        self.ui.reset.setDisabled(True)
        if self.trackingData:
            self.ui.reset.setDisabled(False)

    def syncTolerance(
        self, color: str, source: QSpinBox | QSlider, target: QSpinBox | QSlider
    ):
        val = source.value()

        # Update the data model
        setattr(self.data.tolerances, color, val / 100.0)

        # Update the "buddy" widget without triggering its signal
        _ = target.blockSignals(True)
        target.setValue(val)
        _ = target.blockSignals(False)
