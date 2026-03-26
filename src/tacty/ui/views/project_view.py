import cv2
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QSizePolicy,
    QToolBox,
    QWidget,
)

from tacty.ui.components.video_player import VideoPlayer
from tacty.ui.models.project import Project


class ProjectView(QWidget):
    project: Project
    video: cv2.VideoCapture

    player: VideoPlayer
    sidebar: QToolBox
    calibrationIdx: int
    imageProcessingIdx: int
    trackingIdx: int
    dataProcessingIdx: int
    exportIdx: int

    def __init__(self, project: Project):
        super().__init__()
        self.project = project

        self.video = cv2.VideoCapture(project.videoFile, cv2.CAP_FFMPEG)

        layout = QHBoxLayout()
        self.setLayout(layout)

        # sidebar
        self.sidebar = QToolBox()
        self.sidebar.setMinimumWidth(300)
        self.sidebar.setMaximumWidth(600)
        layout.addWidget(self.sidebar)
        self.calibrationIdx = self.sidebar.addItem(QLabel("1"), "1. Calibration")
        self.imageProcessingIdx = self.sidebar.addItem(
            QLabel("2"), "2. Image processing"
        )
        self.trackingIdx = self.sidebar.addItem(QLabel("3"), "3. Tracking")
        self.dataProcessingIdx = self.sidebar.addItem(QLabel("4"), "4. Data processing")
        self.exportIdx = self.sidebar.addItem(QLabel("5"), "5. Export")

        # video player
        self.player = VideoPlayer(project, self.video)
        layout.addWidget(self.player)
