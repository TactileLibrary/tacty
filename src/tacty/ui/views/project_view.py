import cv2
from PySide6.QtWidgets import QVBoxLayout, QWidget

from tacty.ui.components.video_player import VideoPlayer
from tacty.ui.models.project import Project


class ProjectView(QWidget):
    project: Project
    video: cv2.VideoCapture

    def __init__(self, project: Project):
        super().__init__()
        self.project = project

        self.video = cv2.VideoCapture(project.videoFile, cv2.CAP_FFMPEG)

        layout = QVBoxLayout()
        self.setLayout(layout)

        layout.addWidget(VideoPlayer(project, self.video))
