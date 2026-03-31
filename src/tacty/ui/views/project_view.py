import cv2
from PySide6.QtWidgets import (
    QDialog,
    QHBoxLayout,
    QLabel,
    QProgressDialog,
    QToolBox,
    QWidget,
)

from tacty.ui.components.video_player import VideoPlayer
from tacty.ui.forms.calibration_form import CalibrationForm
from tacty.ui.forms.tracking_form import TrackingForm
from tacty.ui.models.project import Project
from tacty.ui.opencv.tracking_pipeline import TrackingPipeline
from tacty.ui.windows import CornerPickModal


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
    tracking: TrackingForm
    trackingIdx: int
    dataProcessingIdx: int
    exportIdx: int

    # tracking
    modal: QProgressDialog | None = None
    tracker: TrackingPipeline | None = None

    def __init__(self, project: Project):
        super().__init__()
        self.project = project
        self.video = cv2.VideoCapture(project.videoFile, cv2.CAP_FFMPEG)

        layout = QHBoxLayout()
        self.setLayout(layout)

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

        self.imageProcessingIdx = self.sidebar.addItem(
            QLabel("2"), "2. Image processing"
        )

        self.tracking = TrackingForm()
        self.trackingIdx = self.sidebar.addItem(self.tracking, "3. Tracking")
        _ = self.tracking.startProcessing.connect(self.startTracking)

        self.dataProcessingIdx = self.sidebar.addItem(QLabel("4"), "4. Data processing")

        self.exportIdx = self.sidebar.addItem(QLabel("5"), "5. Export")

        # video player
        self.player = VideoPlayer(project, self.video)
        layout.addWidget(self.player)

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

        self.tracker = TrackingPipeline(self.project)

        _ = self.tracker.progress.connect(self.modal.setValue)
        _ = self.tracker.finished.connect(self.modal.close)
        _ = self.modal.canceled.connect(self.tracker.requestInterruption)

        self.tracker.start()

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
