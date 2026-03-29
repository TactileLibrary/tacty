import time
from typing import override

from cv2.typing import MatLike
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QPixmap, QResizeEvent
from PySide6.QtWidgets import (
    QDialog,
    QDialogButtonBox,
    QLabel,
    QSizePolicy,
    QVBoxLayout,
)

from tacty.ui.components.corner_overlay import CornerOverlay
from tacty.ui.models.project import Corners, Size
from tacty.ui.utils.cvConversions import cvToQ

MAX_FPS = 1000 // 30


class CornerPickModal(QDialog):
    buttonBox: QDialogButtonBox
    display: QLabel
    overlay: CornerOverlay
    image: MatLike
    corners: Corners

    # throttle mechanism
    updateTimer: QTimer
    processingTime: int

    def __init__(self, corners: Corners, image: MatLike):
        super().__init__()
        self.image = image
        self.corners = corners

        # set properties
        self.setModal(True)
        self.setMinimumWidth(900)
        self.setMinimumHeight(450)
        self.setWindowTitle("Crop area")

        # set up throttling
        self.updateTimer = QTimer()
        self.updateTimer.setSingleShot(True)
        self.updateTimer.setTimerType(Qt.TimerType.PreciseTimer)
        _ = self.updateTimer.timeout.connect(self.updateDisplay)
        self.processingTime = MAX_FPS

        # add the image
        layout = QVBoxLayout()
        self.setLayout(layout)
        self.display = QLabel()
        self.display.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.display.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding
        )
        self.scheduleUpdateDisplay()
        layout.addWidget(self.display)

        # add the overlay
        h: int
        w: int
        h, w = self.image.shape[:2]  # pyright: ignore [reportAny] have to do thiss due to C bindings
        self.overlay = CornerOverlay(
            corners=self.corners, resolution=Size(w=w, h=h), parent=self.display
        )

        # add buttons
        self.buttonBox = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel,
            self,
        )
        self.buttonBox.button(QDialogButtonBox.StandardButton.Ok).setDefault(True)
        _ = self.buttonBox.accepted.connect(self.accept)
        _ = self.buttonBox.rejected.connect(self.reject)
        layout.addWidget(self.buttonBox)

    def scheduleUpdateDisplay(self) -> None:
        if not self.updateTimer.isActive():
            self.updateTimer.start(max(self.processingTime * 2, MAX_FPS))

    def updateDisplay(self) -> None:
        startTime = time.time()
        qimg = cvToQ(self.image)
        pixmap = QPixmap.fromImage(qimg)
        # very slow, resizing in OpenCV now
        # maybe fine actually?
        pixmap = pixmap.scaled(
            self.display.size(),
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation,
        )
        self.display.setPixmap(pixmap)
        self.updateOverlayGeo()
        endTime = time.time()
        self.processingTime = int((endTime - startTime) * 1000)

    def updateOverlayGeo(self):
        pix = self.display.pixmap()

        label_w = self.display.width()
        label_h = self.display.height()
        video_w = pix.width()
        video_h = pix.height()

        x = (label_w - video_w) // 2
        y = (label_h - video_h) // 2

        self.overlay.setGeometry(x, y, video_w, video_h)

    def getData(self) -> Corners:
        return self.corners

    @override
    def resizeEvent(self, event: QResizeEvent, /) -> None:
        self.scheduleUpdateDisplay()
        super().resizeEvent(event)
        self.updateOverlayGeo()
