from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QMouseEvent, QPixmap
from PySide6.QtWidgets import QDialog, QLabel, QVBoxLayout, QWidget


class HuePickModal(QDialog):
    img: QPixmap
    selected: int | None = None
    display: QLabel

    def __init__(self, pixmap: QPixmap, parent: QWidget | None = None):
        super().__init__(parent)
        self.setWindowTitle("Pick Hue")
        self.setModal(True)

        self.img = pixmap

        layout = QVBoxLayout(self)
        self.display = QLabel()
        self.display.setPixmap(self.img)
        self.display.setCursor(Qt.CursorShape.CrossCursor)
        layout.addWidget(self.display)

        self.display.mousePressEvent = self.getHue

    def getHue(self, event: QMouseEvent) -> None:
        pos = event.pos()
        img = self.img.toImage()

        if 0 <= pos.x() < img.width() and 0 <= pos.y() < img.height():
            color = QColor(img.pixel(pos.x(), pos.y()))
            self.selected = color.hue()

            if self.selected != -1:  # can be -1 if neutral color pressed i think
                self.accept()

    @staticmethod
    def pickHue(pixmap: QPixmap, parent: QWidget | None = None) -> int | None:
        dialog = HuePickModal(pixmap, parent)
        if dialog.exec() == QDialog.DialogCode.Accepted and dialog.selected:
            return dialog.selected // 2
        return None
