from typing import override

from PySide6.QtCore import QEvent, QPoint, Qt
from PySide6.QtGui import QColor, QMouseEvent, QPainter, QPen, QPolygon
from PySide6.QtWidgets import QWidget

from tacty.models.project import Point, Size
from tacty.utils.cvConversions import toSpace


class RectangleOverlay(QWidget):
    tl: Point
    br: Point
    resolution: Size
    pageSize: Size
    points: list[QPoint] = []
    draggedPointIdx: int | None = None

    def __init__(
        self,
        tl: Point,
        br: Point,
        pageSize: Size,
        parent: QWidget | None = None,
    ):
        super().__init__(parent)
        self.tl = tl
        self.br = br
        self.pageSize = pageSize
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
        for i, pt in enumerate(self.points):
            # only render the interactable ones
            if i in (0, 2):
                painter.drawEllipse(pt, 6, 6)

    @override
    def mousePressEvent(self, event: QMouseEvent):
        pos = event.position().toPoint()
        for i, pt in enumerate(self.points):
            # only make tl and br draggable
            if i in (0, 2) and (pt - pos).manhattanLength() < 30:
                self.draggedPointIdx = i
                break

    @override
    def mouseMoveEvent(self, event: QMouseEvent):
        if self.draggedPointIdx is not None:
            new_pos = event.position().toPoint()
            self.points[self.draggedPointIdx] = new_pos

            # enforce other points
            if self.draggedPointIdx == 0:
                self.points[1] = QPoint(self.points[2].x(), new_pos.y())
                self.points[3] = QPoint(new_pos.x(), self.points[2].y())
            elif self.draggedPointIdx == 2:
                self.points[1] = QPoint(new_pos.x(), self.points[0].y())
                self.points[3] = QPoint(self.points[0].x(), new_pos.y())

            self.pointsToCorners()
            self.update()

    @override
    def mouseReleaseEvent(self, event: QMouseEvent):
        self.draggedPointIdx = None

        # normalize to keep tl and br actually tl and br
        x_min, x_max = sorted([self.tl.x, self.br.x])
        y_min, y_max = sorted([self.tl.y, self.br.y])
        self.tl.x, self.tl.y = x_min, y_min
        self.br.x, self.br.y = x_max, y_max

        # redraw to update handles
        self.update()

    def pointsToCorners(self):
        geo = self.rect()
        size = Size(w=geo.width(), h=geo.height())

        # going straight to physical size
        tl = toSpace(self.points[0], size, self.pageSize)
        br = toSpace(self.points[2], size, self.pageSize)

        self.tl = tl
        self.br = br

    def cornersToPoints(self):
        geo = self.rect()
        size = Size(w=geo.width(), h=geo.height())

        tl = toSpace(self.tl, self.pageSize, size)
        br = toSpace(self.br, self.pageSize, size)

        self.points = [
            QPoint(tl.x, tl.y),
            QPoint(br.x, tl.y),
            QPoint(br.x, br.y),
            QPoint(tl.x, br.y),
        ]

    def getData(self):
        return self.tl, self.br
