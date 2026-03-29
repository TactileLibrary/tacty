from PySide6.QtCore import Signal
from PySide6.QtWidgets import QWidget

from tacty.ui.forms.calibration_ui import Ui_Form
from tacty.ui.models.project import CalibrationOptions


class CalibrationForm(QWidget):
    ui: Ui_Form
    data: CalibrationOptions

    dataChanged: Signal = Signal()
    requestInteractiveCornerPicking: Signal = Signal()

    def __init__(self, data: CalibrationOptions):
        super().__init__()

        # load the ui
        self.ui = Ui_Form()
        _ = self.ui.setupUi(self)  # pyright: ignore [reportUnknownMemberType]

        # update the data
        self.data = data
        self.updateData()

        # connectors
        _ = self.ui.startFrame.editingFinished.connect(self.updateStartFrame)
        _ = self.ui.startFrameReset.clicked.connect(self.resetStartFrame)
        _ = self.ui.endFrame.editingFinished.connect(self.updateEndFrame)
        _ = self.ui.endFrameReset.clicked.connect(self.resetEndFrame)
        _ = self.ui.frameRate.editingFinished.connect(self.updateFrameRate)
        _ = self.ui.frameRateReset.clicked.connect(self.resetFrameRate)

        _ = self.ui.topLeftX.editingFinished.connect(self.updateCorners)
        _ = self.ui.topLeftY.editingFinished.connect(self.updateCorners)
        _ = self.ui.topLeftReset.clicked.connect(self.resetTopLeft)
        _ = self.ui.topRightX.editingFinished.connect(self.updateCorners)
        _ = self.ui.topRightY.editingFinished.connect(self.updateCorners)
        _ = self.ui.topRightReset.clicked.connect(self.resetTopRight)
        _ = self.ui.bottomLeftX.editingFinished.connect(self.updateCorners)
        _ = self.ui.bottomLeftY.editingFinished.connect(self.updateCorners)
        _ = self.ui.bottomLeftReset.clicked.connect(self.resetBottomLeft)
        _ = self.ui.bottomRightX.editingFinished.connect(self.updateCorners)
        _ = self.ui.bottomRightY.editingFinished.connect(self.updateCorners)
        _ = self.ui.bottomRightReset.clicked.connect(self.resetBottomRight)
        _ = self.ui.cornerSelect.clicked.connect(self.requestInteractiveCornerPicking)

    def updateData(self):
        # time controls
        self.ui.startFrame.setMaximum(self.data.videoFrameCount)
        self.ui.startFrame.setValue(self.data.videoTrim.start.value)
        self.ui.endFrame.setMaximum(self.data.videoFrameCount)
        self.ui.endFrame.setValue(self.data.videoTrim.end.value)
        self.ui.frameRate.setValue(self.data.videoFps.value)

        # crop controls
        self.ui.topLeftX.setMinimum(0)
        self.ui.topLeftX.setMaximum(self.data.videoCrop.tr.default.x)
        self.ui.topLeftX.setValue(self.data.videoCrop.tl.value.x)
        self.ui.topLeftY.setMinimum(0)
        self.ui.topLeftY.setMaximum(self.data.videoCrop.bl.default.y)
        self.ui.topLeftY.setValue(self.data.videoCrop.tl.value.y)

        self.ui.topRightX.setMinimum(0)
        self.ui.topRightX.setMaximum(self.data.videoCrop.tr.default.x)
        self.ui.topRightX.setValue(self.data.videoCrop.tr.value.x)
        self.ui.topRightY.setMinimum(0)
        self.ui.topRightY.setMaximum(self.data.videoCrop.br.default.y)
        self.ui.topRightY.setValue(self.data.videoCrop.tr.value.y)

        self.ui.bottomLeftX.setMinimum(0)
        self.ui.bottomLeftX.setMaximum(self.data.videoCrop.br.default.x)
        self.ui.bottomLeftX.setValue(self.data.videoCrop.bl.value.x)
        self.ui.bottomLeftY.setMinimum(0)
        self.ui.bottomLeftY.setMaximum(self.data.videoCrop.bl.default.y)
        self.ui.bottomLeftY.setValue(self.data.videoCrop.bl.value.y)

        self.ui.bottomRightX.setMinimum(0)
        self.ui.bottomRightX.setMaximum(self.data.videoCrop.br.default.x)
        self.ui.bottomRightX.setValue(self.data.videoCrop.br.value.x)
        self.ui.bottomRightY.setMinimum(0)
        self.ui.bottomRightY.setMaximum(self.data.videoCrop.br.default.y)
        self.ui.bottomRightY.setValue(self.data.videoCrop.br.value.y)

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

    def updateCorners(self):
        self.data.videoCrop.tl.value.x = self.ui.topLeftX.value()
        self.data.videoCrop.tl.value.y = self.ui.topLeftY.value()
        self.data.videoCrop.tr.value.x = self.ui.topRightX.value()
        self.data.videoCrop.tr.value.y = self.ui.topRightY.value()
        self.data.videoCrop.bl.value.x = self.ui.bottomLeftX.value()
        self.data.videoCrop.bl.value.y = self.ui.bottomLeftY.value()
        self.data.videoCrop.br.value.x = self.ui.bottomRightX.value()
        self.data.videoCrop.br.value.y = self.ui.bottomRightY.value()
        self.dataChanged.emit()

    def resetTopLeft(self):
        self.ui.topLeftX.setValue(self.data.videoCrop.tl.default.x)
        self.ui.topLeftY.setValue(self.data.videoCrop.tl.default.y)
        self.updateCorners()

    def resetTopRight(self):
        self.ui.topRightX.setValue(self.data.videoCrop.tr.default.x)
        self.ui.topRightY.setValue(self.data.videoCrop.tr.default.y)
        self.updateCorners()

    def resetBottomLeft(self):
        self.ui.bottomLeftX.setValue(self.data.videoCrop.bl.default.x)
        self.ui.bottomLeftY.setValue(self.data.videoCrop.bl.default.y)
        self.updateCorners()

    def resetBottomRight(self):
        self.ui.bottomRightX.setValue(self.data.videoCrop.br.default.x)
        self.ui.bottomRightY.setValue(self.data.videoCrop.br.default.y)
        self.updateCorners()
