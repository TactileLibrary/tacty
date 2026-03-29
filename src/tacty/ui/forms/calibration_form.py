from PySide6.QtCore import Signal
from PySide6.QtWidgets import QWidget

from tacty.ui.forms.calibration_ui import Ui_Form
from tacty.ui.models.project import CalibrationOptions


class CalibrationForm(QWidget):
    ui: Ui_Form
    data: CalibrationOptions

    dataChanged: Signal = Signal()

    def __init__(self, data: CalibrationOptions):
        super().__init__()

        # load the ui
        self.ui = Ui_Form()
        _ = self.ui.setupUi(self)  # pyright: ignore [reportUnknownMemberType]

        # update the data
        self.updateData(data)

        # connectors
        _ = self.ui.startFrame.editingFinished.connect(self.updateStartFrame)
        _ = self.ui.startFrameReset.clicked.connect(self.resetStartFrame)
        _ = self.ui.endFrame.editingFinished.connect(self.updateEndFrame)
        _ = self.ui.endFrameReset.clicked.connect(self.resetEndFrame)
        _ = self.ui.frameRate.editingFinished.connect(self.updateFrameRate)
        _ = self.ui.frameRateReset.clicked.connect(self.resetFrameRate)

    def updateData(self, data: CalibrationOptions):
        self.data = data

        self.ui.startFrame.setMaximum(data.videoFrameCount)
        self.ui.startFrame.setValue(data.videoTrim.start.value)
        self.ui.endFrame.setMaximum(data.videoFrameCount)
        self.ui.endFrame.setValue(data.videoTrim.end.value)
        self.ui.frameRate.setValue(data.videoFps.value)

    def updateStartFrame(self, frame: int | None = None):
        if frame is None:
            frame = self.ui.startFrame.value()
        else:
            self.ui.startFrame.setValue(frame)
        self.ui.endFrame.setValue(max(frame, self.ui.endFrame.value()))
        self.data.videoTrim.start.value = frame
        self.dataChanged.emit()

    def resetStartFrame(self):
        frame = self.data.videoTrim.start.default
        self.updateStartFrame(frame)

    def updateEndFrame(self, frame: int | None = None):
        if frame is None:
            frame = self.ui.endFrame.value()
        else:
            self.ui.endFrame.setValue(frame)
        self.ui.startFrame.setValue(min(frame, self.ui.startFrame.value()))
        self.data.videoTrim.end.value = frame
        self.dataChanged.emit()

    def resetEndFrame(self):
        frame = self.data.videoTrim.end.default
        self.updateEndFrame(frame)

    def updateFrameRate(self, fps: float | None = None):
        if fps is None:
            fps = self.ui.frameRate.value()
        else:
            self.ui.frameRate.setValue(fps)
        self.data.videoFps.value = fps
        self.dataChanged.emit()

    def resetFrameRate(self):
        fps = self.data.videoFps.default
        self.updateFrameRate(fps)
