from PySide6.QtWidgets import QLabel, QVBoxLayout, QWidget

from tacty.ui.components.video_player import VideoPlayer
from tacty.ui.models.project import Project


class ProjectView(QWidget):
    project: Project

    def __init__(self, project: Project):
        super().__init__()
        self.project = project

        layout = QVBoxLayout()
        self.setLayout(layout)

        layout.addWidget(VideoPlayer(project))
