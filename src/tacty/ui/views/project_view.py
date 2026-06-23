from pathlib import Path

import cv2
from cv2.typing import MatLike
from PySide6.QtCore import Signal
from PySide6.QtWidgets import (
    QDialog,
    QHBoxLayout,
    QProgressDialog,
    QToolBox,
    QWidget,
)

from tacty.models.project import Project
from tacty.opencv.tracking_pipeline import TrackingPipeline
from tacty.pandas.post_pipeline import PostProcessingPipeline
from tacty.ui.components.video_player import VideoPlayer
from tacty.ui.forms.calibration_form import CalibrationForm
from tacty.ui.forms.export_form import ExportForm
from tacty.ui.forms.postprocessing_form import PostProcessingForm
from tacty.ui.forms.preprocessing_form import PreProcessingForm
from tacty.ui.forms.tracking_form import TrackingForm
from tacty.ui.windows import CornerPickModal
from tacty.ui.windows.rectangle_pick_modal import RectanglePickModal


class ProjectView(QWidget):
    # project data
    project: Project
    video: cv2.VideoCapture

    # widgets
    player: VideoPlayer
    sidebar: QToolBox
    calibrationIdx: int
    calibration: CalibrationForm
    imageProcessingIdx: int
    imageProcessing: PreProcessingForm
    tracking: TrackingForm
    trackingIdx: int
    dataProcessing: PostProcessingForm
    dataProcessingIdx: int
    export: ExportForm
    exportIdx: int

    # debug
    debugImages: dict[str, MatLike]
    debugTracker: TrackingPipeline
    debugMode: bool = False

    # signals
    debugChanged: Signal = Signal()

    # tracking
    modal: QProgressDialog | None = None
    tracker: TrackingPipeline | None = None

    # post processing
    dataProcessor: PostProcessingPipeline

    def __init__(self, project: Project, debugImages: dict[str, MatLike]):
        super().__init__()
        self.project = project
        self.debugImages = debugImages
        self.video = cv2.VideoCapture(project.videoFile, cv2.CAP_FFMPEG)
        self.dataProcessor = PostProcessingPipeline(self.project)

        layout = QHBoxLayout()
        self.setLayout(layout)

        self.player = VideoPlayer(project, self.video, debugImages)
        self.debugTracker = TrackingPipeline(self.project, self.debugImages)

        # sidebar
        self.sidebar = QToolBox()
        self.sidebar.setMinimumWidth(400)
        self.sidebar.setMaximumWidth(600)
        layout.addWidget(self.sidebar)

        self.calibration = CalibrationForm(self.project.calibrationOptions)
        self.calibrationIdx = self.sidebar.addItem(self.calibration, "1. Calibration")
        _ = self.calibration.dataChanged.connect(self.updateProject)
        _ = self.calibration.requestInteractiveCornerPicking.connect(
            self.openInteractivePicker
        )

        self.imageProcessing = PreProcessingForm(self.project.preProcessingOptions, self.project.calibrationOptions.videoTrim.end.default)
        self.imageProcessingIdx = self.sidebar.addItem(self.imageProcessing, "2. Image processing")

        self.tracking = TrackingForm(
            self.project.trackingOptions,
            len(self.project.trackingData.keys()) > 0,
            self.player,
        )
        self.trackingIdx = self.sidebar.addItem(self.tracking, "3. Tracking")
        _ = self.tracking.startProcessing.connect(self.startTracking)
        _ = self.tracking.resetTrackingData.connect(self.resetTracking)

        self.dataProcessing = PostProcessingForm(self.project.postProcessingOptions)
        self.dataProcessingIdx = self.sidebar.addItem(
            self.dataProcessing, "4. Data processing"
        )
        _ = self.dataProcessing.dataChanged.connect(self.processData)
        _ = self.dataProcessing.requestRect.connect(self.getRectAOI)

        self.export = ExportForm()
        self.exportIdx = self.sidebar.addItem(self.export, "5. Export")

        # video player
        layout.addWidget(self.player)
        _ = self.player.frameChanged.connect(self.updateDebugImages)

        self.processData()

    def getRectAOI(self):
        img = self.player.getImage()
        if img is None:
            return
        dialog = RectanglePickModal(
            image=img, pageSize=self.project.calibrationOptions.pageSize
        )
        res = dialog.exec()
        if res == QDialog.DialogCode.Rejected:
            return
        tl, br = dialog.getData()

        self.dataProcessing.addRectangleAOI(tl, br)

    def updateDebugImages(self):
        if not self.debugMode:
            return

        # reset images
        self.debugImages.clear()

        # tell components to add images
        self.player.addDebugImages()
        img = self.player.getImage()
        if img is not None:
            self.debugTracker.updateDebugImages(img)

        # tell window to update menu
        self.debugChanged.emit()

    def startTracking(self):
        self.modal = QProgressDialog(
            "Tracking...",
            "Cancel",
            self.project.calibrationOptions.videoTrim.start.value,
            self.project.calibrationOptions.videoTrim.end.value,
            self,
        )
        self.modal.setModal(True)
        self.modal.setMinimumDuration(0)

        self.tracker = TrackingPipeline(self.project, self.debugImages)

        _ = self.tracker.progress.connect(self.modal.setValue)
        _ = self.tracker.finished.connect(self.trackingFinished)
        _ = self.modal.canceled.connect(self.tracker.requestInterruption)

        self.tracker.start()

    def processData(self) -> None:
        data = None
        if len(self.project.trackingData.keys()) > 0:
            data = self.dataProcessor.processs()
        self.player.updateData(data)
        self.player.updateDisplay()
        self.export.updateData(
            data,
            self.project.calibrationOptions.videoFps.value,
            Path(self.project.videoFile).name,
        )

    def trackingFinished(self):
        if self.modal:
            _ = self.modal.close()

        self.tracking.trackingData = len(self.project.trackingData.keys()) > 0
        self.tracking.updateData()
        self.processData()

    def resetTracking(self):
        self.project.trackingData = {}
        self.tracking.trackingData = False
        self.tracking.updateData()
        self.processData()

    def updateProject(self):
        self.player.updateProject()
        self.calibration.updateData()

    def openInteractivePicker(self):
        if self.player.img is None:
            return
        dialog = CornerPickModal(
            corners=self.project.calibrationOptions.videoCrop.model_copy(deep=True),
            image=self.player.img,
        )
        res = dialog.exec()
        if res == QDialog.DialogCode.Rejected:
            return

        newCorners = dialog.getData()
        self.project.calibrationOptions.videoCrop = newCorners
        self.updateProject()
