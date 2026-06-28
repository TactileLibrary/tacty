from typing import override

from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QMouseEvent, QPixmap, QResizeEvent
from PySide6.QtWidgets import QDialog, QLabel, QSizePolicy, QVBoxLayout, QWidget


class HuePickModal(QDialog):
    img: QPixmap
    selected: int | None = None
    display: QLabel

    def __init__(self, pixmap: QPixmap, parent: QWidget | None = None):
        super().__init__(parent)
        self.setWindowTitle("Pick Hue")
        self.setModal(True)
        self.setMinimumWidth(900)
        self.setMinimumHeight(450)

        self.img = pixmap

        layout = QVBoxLayout(self)
        self.display = QLabel()
        self.display.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.display.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding
        )
        self.display.setCursor(Qt.CursorShape.CrossCursor)
        layout.addWidget(self.display)

        self.display.mousePressEvent = self.getHue

    def updateDisplay(self) -> None:     
        scaled_pixmap = self.img.scaled(
            self.display.size(),
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation,
        )
        self.display.setPixmap(scaled_pixmap)

    @override
    def resizeEvent(self, event: QResizeEvent) -> None:
        super().resizeEvent(event)
        self.updateDisplay()

    def getHue(self, event: QMouseEvent) -> None:
        pix = self.display.pixmap()

        label_w = self.display.width()
        label_h = self.display.height()
        scaled_w = pix.width()
        scaled_h = pix.height()
        og_w = self.img.width()
        og_h = self.img.height()

        offset_x = (label_w - scaled_w) // 2
        offset_y = (label_h - scaled_h) // 2

        click_x = event.pos().x() - offset_x
        click_y = event.pos().y() - offset_y


        if 0 <= click_x < scaled_w and 0 <= click_y < scaled_h:
            og_x = int(click_x * og_w / scaled_w)
            og_y = int(click_y * og_h / scaled_h)

            og_x = max(0, min(og_x, og_w - 1))
            og_y = max(0, min(og_y, og_h - 1))

            color = QColor(self.img.toImage().pixel(og_x, og_y))
            self.selected = color.hue()

            if self.selected != -1:  # can be -1 if neutral color pressed i think
                self.accept()

    @staticmethod
    def pickHue(pixmap: QPixmap, parent: QWidget | None = None) -> int | None:
        dialog = HuePickModal(pixmap, parent)
        if dialog.exec() == QDialog.DialogCode.Accepted and dialog.selected is not None:
            return dialog.selected // 2
        return None
