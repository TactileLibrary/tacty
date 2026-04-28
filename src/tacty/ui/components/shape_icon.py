from PySide6.QtCore import QSize
from PySide6.QtGui import QBrush, QColor, QIcon, QPainter, QPixmap, Qt


def getShapeIcon(color: str, shape: str, size: int = 32, padding: int = 2) -> QIcon:
    pixmap = QPixmap(QSize(size, size))
    pixmap.fill(Qt.GlobalColor.transparent)

    painter = QPainter(pixmap)
    painter.setRenderHint(QPainter.RenderHint.Antialiasing)
    painter.setBrush(QBrush(QColor(color)))  # should work with the basic color names
    painter.setPen(Qt.PenStyle.NoPen)

    if shape == "circle":
        painter.drawEllipse(padding, padding, size - padding * 2, size - padding * 2)
    else:
        painter.drawRect(padding, padding, size - padding * 2, size - padding * 2)

    _ = painter.end()
    return QIcon(pixmap)
