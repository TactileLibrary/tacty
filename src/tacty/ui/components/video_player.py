from PySide6.QtCore import Qt
from PySide6.QtWidgets import QHBoxLayout, QLabel, QSlider, QVBoxLayout, QWidget

from tacty.ui.models.project import Duration, Project


class VideoPlayer(QWidget):
    project: Project
    frame: int = 0
    display: QLabel
    slider: QSlider
    frameDisplay: QLabel

    def __init__(self, project: Project):
        super().__init__()

        mainLayout = QHBoxLayout()
        self.setLayout(mainLayout)

        # video display
        self.display = QLabel()
        mainLayout.addWidget(self.display)

        # control slider
        timeline = QWidget()
        timelineLayout = QVBoxLayout()
        timeline.setLayout(timelineLayout)
        mainLayout.addWidget(timeline)
        self.slider = QSlider(Qt.Orientation.Horizontal)
        _ = self.slider.sliderMoved.connect(self.updateFrame)
        timelineLayout.addWidget(self.slider)
        self.frameDisplay = QLabel()
        timelineLayout.addWidget(self.frameDisplay)

        self.updateProject(project)

    def updateFrame(self, frame: int) -> None:
        frame = min(
            self.project.calibrationOptions.videoTrim.end,
            max(self.project.calibrationOptions.videoTrim.start, frame),
        )
        print(self.project.calibrationOptions.videoTrim.start)
        self.frameDisplay.setText(str(frame))
        self.frame = frame

    def updateTimelineBounds(self) -> None:
        self.slider.setMinimum(self.project.calibrationOptions.videoTrim.start)
        self.slider.setMaximum(self.project.calibrationOptions.videoTrim.end)

    def updateProject(self, project: Project) -> None:
        self.project = project
        self.updateTimelineBounds()
        self.updateFrame(self.frame)
