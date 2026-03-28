import time
from typing import override

import cv2
from cv2 import VideoCapture
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QFont, QPixmap, QResizeEvent
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QSizePolicy,
    QSlider,
    QVBoxLayout,
    QWidget,
)

from tacty.ui.models.project import Project
from tacty.ui.utils.conversions import cvToQ

MAX_FPS = 1000 // 30


class VideoPlayer(QWidget):
    project: Project
    frame: int = 0
    display: QLabel
    slider: QSlider
    frameDisplay: QLabel
    video: VideoCapture
    videoFrameCountDigits: int

    # throttle mechanism
    updateTimer: QTimer
    processingTime: int

    def __init__(self, project: Project, video: VideoCapture):
        super().__init__()

        mainLayout = QVBoxLayout()
        self.setLayout(mainLayout)
        self.video = video
        self.videoFrameCountDigits = len(
            str(project.calibrationOptions.videoFrameCount)
        )

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

        monoFont = QFont()
        monoFont.setStyleHint(QFont.StyleHint.Monospace)
        self.frameDisplay = QLabel()
        self.frameDisplay.setFont(monoFont)
        self.frameDisplay.setFrameShape(QFrame.Shape.StyledPanel)
        timelineLayout.addWidget(self.frameDisplay)

        self.updateTimer = QTimer()
        self.updateTimer.setSingleShot(True)
        self.updateTimer.setTimerType(Qt.TimerType.PreciseTimer)
        _ = self.updateTimer.timeout.connect(self.updateDisplay)
        self.processingTime = MAX_FPS

        self.updateProject(project)

    def updateFrame(self, frame: int) -> None:
        frame = min(
            self.project.calibrationOptions.videoTrim.end,
            max(self.project.calibrationOptions.videoTrim.start, frame),
        )
        self.frame = frame
        frameText = str(frame).rjust(self.videoFrameCountDigits, "0")
        self.frameDisplay.setText(frameText)
        self.scheduleUpdateDisplay()

    def scheduleUpdateDisplay(self) -> None:
        if not self.updateTimer.isActive():
            self.updateTimer.start(max(self.processingTime * 2, MAX_FPS))

    def updateDisplay(self) -> None:
        startTime = time.time()
        _ = self.video.set(
            cv2.CAP_PROP_POS_FRAMES, self.frame - 1
        )  # -1 because read grabs the NEXT frame
        _, cimg = self.video.read()
        # qimg = cvToQScaled(
        #    cimg, self.display.size().height(), self.display.size().width()
        # )
        qimg = cvToQ(cimg)
        pixmap = QPixmap.fromImage(qimg)
        # very slow, resizing in OpenCV now
        # maybe fine actually?
        pixmap = pixmap.scaled(
            self.display.size(),
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation,
        )
        self.display.setPixmap(pixmap)
        endTime = time.time()
        self.processingTime = int((endTime - startTime) * 1000)

    def updateTimelineBounds(self) -> None:
        self.slider.setMinimum(self.project.calibrationOptions.videoTrim.start)
        self.slider.setMaximum(self.project.calibrationOptions.videoTrim.end)
        self.slider.setTickInterval(round(self.project.calibrationOptions.videoFps))
        self.slider.setTickPosition(QSlider.TickPosition.TicksAbove)

    def updateProject(self, project: Project) -> None:
        self.project = project
        self.updateTimelineBounds()
        self.updateFrame(self.frame)

    @override
    def resizeEvent(self, event: QResizeEvent, /) -> None:
        self.scheduleUpdateDisplay()
        return super().resizeEvent(event)
