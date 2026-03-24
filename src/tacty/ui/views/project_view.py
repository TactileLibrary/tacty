from PySide6.QtWidgets import QLabel, QVBoxLayout, QWidget

from tacty.ui.models.project import Project


class ProjectView(QWidget):
    project: Project

    def __init__(self, project: Project):
        super().__init__()
        self.project = project

        layout = QVBoxLayout()
        self.setLayout(layout)

        layout.addWidget(QLabel(self.project.videoFile))
