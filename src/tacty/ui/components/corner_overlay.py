from typing import override

from PySide6.QtCore import QEvent, QPoint, Qt
from PySide6.QtGui import QColor, QMouseEvent, QPainter, QPen, QPolygon
from PySide6.QtWidgets import QWidget

from tacty.ui.models.project import Corners, Size
from tacty.ui.utils.cvConversions import toSpace


class CornerOverlay(QWidget):
    corners: Corners
    resolution: Size
    points: list[QPoint] = []
    draggedPointIdx: int | None = None

    def __init__(
        self, corners: Corners, resolution: Size, parent: QWidget | None = None
    ):
        super().__init__(parent)
        self.corners = corners
        self.resolution = resolution
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

    @override
    def paintEvent(self, event: QEvent):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        self.cornersToPoints()

        strokeColor = QColor(30, 150, 190, 255)
        fillColor = QColor(30, 150, 190, 50)

        painter.setPen(QPen(strokeColor, 2))
        painter.setBrush(fillColor)
        painter.drawPolygon(QPolygon(self.points))

        # Draw handles
        painter.setBrush(QColor(255, 255, 255))
        for pt in self.points:
            painter.drawEllipse(pt, 6, 6)

    @override
    def mousePressEvent(self, event: QMouseEvent):
        pos = event.position().toPoint()
        for i, pt in enumerate(self.points):
            if (pt - pos).manhattanLength() < 30:
                self.draggedPointIdx = i
                break

    @override
    def mouseMoveEvent(self, event: QMouseEvent):
        if self.draggedPointIdx is not None:
            self.points[self.draggedPointIdx] = event.position().toPoint()
            self.pointsToCorners()
            self.update()

    @override
    def mouseReleaseEvent(self, event: QMouseEvent):
        self.draggedPointIdx = None

    def pointsToCorners(self):
        geo = self.rect()
        size = Size(w=geo.width(), h=geo.height())

        tl = toSpace(self.points[0], size, self.resolution)
        tr = toSpace(self.points[1], size, self.resolution)
        br = toSpace(self.points[2], size, self.resolution)
        bl = toSpace(self.points[3], size, self.resolution)

        self.corners.tl.value = tl
        self.corners.tr.value = tr
        self.corners.br.value = br
        self.corners.bl.value = bl

    def cornersToPoints(self):
        geo = self.rect()
        size = Size(w=geo.width(), h=geo.height())

        tl = toSpace(self.corners.tl.value, self.resolution, size)
        tr = toSpace(self.corners.tr.value, self.resolution, size)
        br = toSpace(self.corners.br.value, self.resolution, size)
        bl = toSpace(self.corners.bl.value, self.resolution, size)

        self.points = [
            QPoint(tl.x, tl.y),
            QPoint(tr.x, tr.y),
            QPoint(br.x, br.y),
            QPoint(bl.x, bl.y),
        ]
