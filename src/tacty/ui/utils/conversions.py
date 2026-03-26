import cv2
from cv2.typing import MatLike
from PySide6.QtGui import QImage


def mmToInch(m: float) -> float:
    return m / 25.4


def cvToQ(frame: MatLike) -> QImage:
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    h: int
    w: int
    c: int
    h, w, c = rgb.shape  # pyright: ignore [reportAny] have to do thiss due to C bindings

    bytesPerLine = c * w

    return QImage(rgb.data, w, h, bytesPerLine, QImage.Format.Format_RGB888)


def cvToQScaled(frame: MatLike, lh: int, lw: int) -> QImage:
    vh: int
    vw: int
    vh, vw = frame.shape[:2]  # pyright: ignore [reportAny] have to do thiss due to C bindings

    s = min(lw / vw, lh / vh)

    h = int(s * vh)
    w = int(s * vw)

    return cvToQ(cv2.resize(frame, (w, h), interpolation=cv2.INTER_NEAREST))
