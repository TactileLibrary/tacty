from typing import override

import cv2
from cv2 import VideoCapture
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap, QResizeEvent
from PySide6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QSizePolicy,
    QSlider,
    QVBoxLayout,
    QWidget,
)

from tacty.ui.models.project import Project
from tacty.ui.utils.conversions import cvToQScaled


class VideoPlayer(QWidget):
    project: Project
    frame: int = 0
    display: QLabel
    slider: QSlider
    frameDisplay: QLabel
    video: VideoCapture

    def __init__(self, project: Project, video: VideoCapture):
        super().__init__()

        mainLayout = QVBoxLayout()
        self.setLayout(mainLayout)
        self.video = video

        # video display
        self.display = QLabel()
        self.display.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.display.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding
        )
        mainLayout.addWidget(self.display)

        # control slider
        timeline = QWidget()
        timelineLayout = QHBoxLayout()
        timeline.setLayout(timelineLayout)
        mainLayout.addWidget(timeline)
        self.slider = QSlider(Qt.Orientation.Horizontal)
        _ = self.slider.valueChanged.connect(self.updateFrame)
        timelineLayout.addWidget(self.slider)
        self.frameDisplay = QLabel()
        timelineLayout.addWidget(self.frameDisplay)

        self.updateProject(project)

    def updateFrame(self, frame: int) -> None:
        frame = min(
            self.project.calibrationOptions.videoTrim.end,
            max(self.project.calibrationOptions.videoTrim.start, frame),
        )
        self.frame = frame
        self.frameDisplay.setText(str(frame))
        self.updateDisplay()

    def updateDisplay(self) -> None:
        _ = self.video.set(
            cv2.CAP_PROP_POS_FRAMES, self.frame - 1
        )  # -1 because read grabs the NEXT frame
        _, cimg = self.video.read()
        qimg = cvToQScaled(
            cimg, self.display.size().height(), self.display.size().width()
        )
        pixmap = QPixmap.fromImage(qimg)
        # very slow, resizing in OpenCV now
        # pixmap = pixmap.scaled(
        #    self.display.size(),
        #    Qt.AspectRatioMode.KeepAspectRatio,
        #    Qt.TransformationMode.SmoothTransformation,
        # )
        self.display.setPixmap(pixmap)

    def updateTimelineBounds(self) -> None:
        self.slider.setMinimum(self.project.calibrationOptions.videoTrim.start)
        self.slider.setMaximum(self.project.calibrationOptions.videoTrim.end)
        self.slider.setTickInterval(100)
        self.slider.setTickPosition(QSlider.TickPosition.TicksAbove)

    def updateProject(self, project: Project) -> None:
        self.project = project
        self.updateTimelineBounds()
        self.updateFrame(self.frame)

    @override
    def resizeEvent(self, event: QResizeEvent, /) -> None:
        self.updateDisplay()
        return super().resizeEvent(event)
