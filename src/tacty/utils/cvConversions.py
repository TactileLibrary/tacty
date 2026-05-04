import cv2
from cv2.typing import MatLike
from PySide6.QtCore import QPoint
from PySide6.QtGui import QImage

from tacty.models.project import Point, Size


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


def toSpace(point: Point | QPoint, og: Size, to: Size) -> Point:
    scale_x = to.w / og.w
    scale_y = to.h / og.h

    if isinstance(point, Point):
        x, y = point.x, point.y
    else:
        x, y = point.x(), point.y()

    return Point(x=round(x * scale_x), y=round(y * scale_y))
