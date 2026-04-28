import time
from typing import override

import cv2
from cv2 import VideoCapture
from cv2.typing import MatLike
from PySide6.QtCore import Qt, QTimer, Signal
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
from tacty.ui.opencv.calibration_pipeline import CalibrationPipeline
from tacty.ui.opencv.tracking_display_pipeline import TrackingDisplayPipeline
from tacty.ui.utils.cvConversions import cvToQ

MAX_FPS = 1000 // 30


class VideoPlayer(QWidget):
    project: Project
    display: QLabel
    slider: QSlider
    frameDisplay: QLabel
    video: VideoCapture
    videoFrameCountDigits: int
    img: MatLike | None = None

    # pipelines
    calibrationPipeline: CalibrationPipeline
    trackingPipeline: TrackingDisplayPipeline

    # throttle mechanism
    updateTimer: QTimer
    processingTime: int

    # signals
    frameChanged: Signal = Signal()

    # debug
    debugImages: dict[str, MatLike]

    def __init__(
        self, project: Project, video: VideoCapture, debugImages: dict[str, MatLike]
    ):
        super().__init__()

        mainLayout = QVBoxLayout()
        self.setLayout(mainLayout)
        self.video = video
        self.videoFrameCountDigits = len(
            str(project.calibrationOptions.videoFrameCount)
        )
        self.calibrationPipeline = CalibrationPipeline(project.calibrationOptions)
        self.trackingPipeline = TrackingDisplayPipeline(project)
        self.debugImages = debugImages

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

        self.project = project
        self.updateProject()

    def updateFrame(self, frame: int) -> None:
        frame = min(
            self.project.calibrationOptions.videoTrim.end.value,
            max(self.project.calibrationOptions.videoTrim.start.value, frame),
        )
        self.project.frame = frame
        self.slider.setValue(frame)
        frameText = str(frame).rjust(self.videoFrameCountDigits, "0")
        self.frameDisplay.setText(frameText)
        self.scheduleUpdateDisplay()
        self.frameChanged.emit()

    def scheduleUpdateDisplay(self) -> None:
        if not self.updateTimer.isActive():
            self.updateTimer.start(max(self.processingTime * 2, MAX_FPS))

    def updateDisplay(self) -> None:
        startTime = time.time()
        _ = self.video.set(cv2.CAP_PROP_POS_FRAMES, self.project.frame)
        _, self.img = self.video.read()

        img = self.calibrationPipeline.process(self.img)
        img = self.trackingPipeline.process(img)

        qimg = cvToQ(img)
        pixmap = QPixmap.fromImage(qimg)
        pixmap = pixmap.scaled(
            self.display.size(),
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation,
        )
        self.display.setPixmap(pixmap)
        endTime = time.time()
        self.processingTime = int((endTime - startTime) * 1000)

    def updateTimelineBounds(self) -> None:
        _ = self.slider.blockSignals(True)
        self.slider.setMinimum(self.project.calibrationOptions.videoTrim.start.value)
        self.slider.setMaximum(self.project.calibrationOptions.videoTrim.end.value)
        self.slider.setTickInterval(
            round(self.project.calibrationOptions.videoFps.value)
        )
        self.slider.setTickPosition(QSlider.TickPosition.TicksAbove)
        _ = self.slider.blockSignals(False)

    def updateProject(self) -> None:
        self.updateTimelineBounds()
        self.updateFrame(self.project.frame)

    def getImage(self) -> MatLike | None:
        if self.img is None:
            return
        img = self.calibrationPipeline.process(self.img)
        return img

    def getPixmap(self) -> QPixmap | None:
        if self.img is None:
            return
        img = self.calibrationPipeline.process(self.img)
        qimg = cvToQ(img)
        pixmap = QPixmap.fromImage(qimg)
        return pixmap

    def addDebugImages(self) -> None:
        if self.img is not None:
            self.debugImages["Original"] = self.img

    @override
    def resizeEvent(self, event: QResizeEvent, /) -> None:
        self.scheduleUpdateDisplay()
        return super().resizeEvent(event)
