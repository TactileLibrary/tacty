from PySide6.QtCore import Signal
from PySide6.QtWidgets import QWidget

from tacty.models.project import CalibrationOptions, Size
from tacty.ui.forms.calibration_ui import Ui_Form


class PageTemplate:
    name: str
    size: Size
    dpi: int

    def __init__(self, name: str, width: int, height: int, dpi: int):
        self.name = name
        self.size = Size(w=width, h=height)
        self.dpi = dpi


PAGE_TEMPLATES = [
    PageTemplate("A3 [Landscape]", 420, 297, 92),
    PageTemplate("A3 [Portrait]", 297, 497, 92),
    PageTemplate("A4 [Landscape]", 297, 210, 130),
    PageTemplate("A4 [Portrait]", 210, 297, 130),
    PageTemplate("Letter [Landdscape]", 279, 216, 120),
    PageTemplate("Letter [Portrait]", 216, 279, 120),
]


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

        _ = self.ui.pageTemplate.currentIndexChanged.connect(self.applyPageTemplate)
        _ = self.ui.pageHeight.valueChanged.connect(self.updatePageSize)
        _ = self.ui.pageWidth.valueChanged.connect(self.updatePageSize)
        _ = self.ui.resolution.valueChanged.connect(self.updateResolution)

        self.setupPageTemplates()
        self.updatePageSize()

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

        # retime controls
        self.ui.pageWidth.setValue(self.data.pageSize.w)
        self.ui.pageHeight.setValue(self.data.pageSize.h)
        self.ui.resolution.setValue(self.data.processingDpi)

    def setupPageTemplates(self):
        for template in PAGE_TEMPLATES:
            self.ui.pageTemplate.addItem(template.name, [template.size, template.dpi])

    def applyPageTemplate(self):
        data = self.ui.pageTemplate.currentData()  # pyright: ignore [reportAny] - we check isinstance anyway
        if data is None:
            return
        size, dpi = data  # pyright: ignore [reportAny] - we check isinstance anyway
        if not (isinstance(size, Size) and isinstance(dpi, int)):
            return

        self.ui.pageWidth.setValue(size.w)
        self.ui.pageHeight.setValue(size.h)
        self.ui.resolution.setValue(dpi)

    def updateResolution(self):
        self.data.processingDpi = self.ui.resolution.value()
        self.ui.resultingSize.setText(self.data.processingResolution().toString())
        self.dataChanged.emit()
        self.updatePageTemplate()

    def updatePageSize(self):
        self.data.pageSize.w = self.ui.pageWidth.value()
        self.data.pageSize.h = self.ui.pageHeight.value()
        self.ui.resultingSize.setText(self.data.processingResolution().toString())
        self.ui.resolution.setMaximum(self.data.maxDpi())
        self.dataChanged.emit()
        self.updatePageTemplate()

    def updatePageTemplate(self):
        # check if it matches a template
        for idx, template in enumerate(PAGE_TEMPLATES):
            if (
                template.size == self.data.pageSize
                and template.dpi == self.data.processingDpi
            ):
                self.ui.pageTemplate.setCurrentIndex(idx + 1)
                return
        self.ui.pageTemplate.setCurrentIndex(0)

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
