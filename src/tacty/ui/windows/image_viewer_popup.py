from cv2.typing import MatLike
from PySide6.QtCore import Qt
from PySide6.QtGui import QKeyEvent
from PySide6.QtWidgets import QDialog, QLabel, QVBoxLayout
from typing_extensions import override

from tacty.ui.components.image_viewer import ImageViewer


class ImageViewerPopup(QDialog):
    viewer: ImageViewer

    def __init__(self, name: str, image: MatLike):
        super().__init__()
        self.setWindowTitle("Debug image viewer - " + name)
        self.resize(800, 450)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)  # Remove borders for a cleaner look

        self.viewer = ImageViewer(image)
        layout.addWidget(self.viewer)

        layout.addWidget(
            QLabel(
                f"Image resolution {image.shape[1]}x{image.shape[0]}. Press 's' to save the image, 'f' to fit it to the screen or 'q' to quit."
            )
        )

        self.fitImage()

    @override
    def keyPressEvent(self, event: QKeyEvent) -> None:
        if event.key() == Qt.Key.Key_F:
            self.fitImage()

        if event.key() == Qt.Key.Key_Q:
            _ = self.close()

    def fitImage(self) -> None:
        self.viewer.fitInView(
            self.viewer.pixmapItem, Qt.AspectRatioMode.KeepAspectRatio
        )
