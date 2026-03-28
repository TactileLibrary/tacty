from PySide6.QtCore import Signal
from PySide6.QtWidgets import QWidget

from tacty.ui.forms.calibration_ui import Ui_Form
from tacty.ui.models.project import CalibrationOptions


class CalibrationForm(QWidget):
    ui: Ui_Form
    data: CalibrationOptions

    dataChanged: Signal = Signal(CalibrationOptions)

    def __init__(self, data: CalibrationOptions):
        super().__init__()

        # load the ui
        self.ui = Ui_Form()
        _ = self.ui.setupUi(self)  # pyright: ignore [reportUnknownMemberType]

        # update the data
        self.updateData(data)

        # connectors
        _ = self.ui.startFrame.editingFinished.connect(self.updateStartFrame)
        _ = self.ui.endFrame.editingFinished.connect(self.updateEndFrame)
        _ = self.ui.frameRate.editingFinished.connect(self.updateFrameRate)

    def updateData(self, data: CalibrationOptions):
        self.data = data

        self.ui.startFrame.setMaximum(data.videoFrameCount)
        self.ui.startFrame.setValue(data.videoTrim.start)
        self.ui.endFrame.setMaximum(data.videoFrameCount)
        self.ui.endFrame.setValue(data.videoTrim.end)
        self.ui.frameRate.setValue(data.videoFps)

    def updateStartFrame(self):
        frame = self.ui.startFrame.value()
        self.ui.endFrame.setValue(max(frame, self.ui.endFrame.value()))
        self.data.videoTrim.start = frame
        self.dataChanged.emit(self.data)

    def updateEndFrame(self):
        frame = self.ui.endFrame.value()
        self.ui.startFrame.setValue(min(frame, self.ui.startFrame.value()))
        self.data.videoTrim.end = frame
        self.dataChanged.emit(self.data)

    def updateFrameRate(self):
        fps = self.ui.frameRate.value()
        self.data.videoFps = fps
        self.dataChanged.emit(self.data)
