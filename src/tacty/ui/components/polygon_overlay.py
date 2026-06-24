from typing import override

from PySide6.QtCore import QEvent, QPoint, Qt, Signal
from PySide6.QtGui import QColor, QMouseEvent, QPainter, QPen, QPolygon
from PySide6.QtWidgets import QWidget

from tacty.models.project import Size, Point
from tacty.utils.cvConversions import toSpace


class PolygonOverlay(QWidget):
    pageSize: Size

    qPoints: list[QPoint] = []
    tPoints: list[Point] = []

    draggedPointIdx: int | None = None
    closed: bool = False

    closedChanged: Signal = Signal()

    def __init__(
        self, tPoints: list[Point], pageSize: Size, parent: QWidget | None = None
    ):
        super().__init__(parent)
        self.tPoints = tPoints
        self.pageSize = pageSize
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

    @override
    def paintEvent(self, event: QEvent):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        self.tPointsToQPoints()

        strokeColor = QColor(30, 150, 190, 255)
        fillColor = QColor(30, 150, 190, 50)

        painter.setPen(QPen(strokeColor, 2))
        painter.setBrush(fillColor)

        if self.closed:
            painter.drawPolygon(QPolygon(self.qPoints))
        else:
            painter.drawPolyline(QPolygon(self.qPoints))

        # Draw handles
        painter.setBrush(QColor(255, 255, 255))
        for pt in self.qPoints:
            painter.drawEllipse(pt, 6, 6)

    @override
    def mousePressEvent(self, event: QMouseEvent):
        # left click for dragging and adding
        if event.button() == Qt.MouseButton.LeftButton:

            pos = event.position().toPoint()
            for i, pt in enumerate(self.qPoints):
                if (pt - pos).manhattanLength() < 30:
                    self.draggedPointIdx = i
                    break

            # if the id is 0 and we have enough points, we mark the loop closed
            if self.draggedPointIdx == 0 and len(self.qPoints) >= 3:
                self.closed = True
                self.closedChanged.emit()

            # if there is no dragged point and the shape isn't closed, we add a new one
            if self.draggedPointIdx is None and not self.closed:
                self.qPoints.append(pos)
                self.draggedPointIdx = len(self.qPoints) - 1

        # right click for removing
        elif event.button() == Qt.MouseButton.RightButton:
            pos = event.position().toPoint()
            for i, pt in enumerate(self.qPoints):
                if (pt - pos).manhattanLength() < 30:
                    self.qPoints.pop(i)
                    self.qPointsToTPoints()
                    break

            # if the shape now has less than 3 points, we mark it as open
            if len(self.qPoints) < 3:
                self.closed = False
                self.closedChanged.emit()

        self.qPointsToTPoints()

    @override
    def mouseMoveEvent(self, event: QMouseEvent):
        if self.draggedPointIdx is not None:
            self.qPoints[self.draggedPointIdx] = event.position().toPoint()
            self.qPointsToTPoints()
            self.update()

    @override
    def mouseReleaseEvent(self, event: QMouseEvent):
        self.draggedPointIdx = None
        self.update()

    def qPointsToTPoints(self):
        geo = self.rect()
        size = Size(w=geo.width(), h=geo.height())

        # reset
        self.tPoints = []

        for i, pt in enumerate(self.qPoints):
            self.tPoints.append(toSpace(pt, size, self.pageSize))



    def tPointsToQPoints(self):
        geo = self.rect()
        size = Size(w=geo.width(), h=geo.height())

        # reset
        self.qPoints = []

        for i, pt in enumerate(self.tPoints):
            point = toSpace(pt, self.pageSize, size)
            self.qPoints.append(QPoint(point.x, point.y))

    def getData(self):
        return self.tPoints