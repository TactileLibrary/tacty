from cv2.typing import MatLike
from PySide6.QtGui import QPainter, QPixmap, QWheelEvent
from PySide6.QtWidgets import QGraphicsPixmapItem, QGraphicsScene, QGraphicsView
from typing_extensions import override

from tacty.utils.cvConversions import cvToQ


class ImageViewer(QGraphicsView):
    graphicsScene: QGraphicsScene
    pixmapItem: QGraphicsPixmapItem

    def __init__(self, image: MatLike):
        super().__init__()
        self.graphicsScene = QGraphicsScene(self)
        self.setScene(self.graphicsScene)

        self.pixmapItem = QGraphicsPixmapItem(QPixmap(cvToQ(image)))

        self.graphicsScene.addItem(self.pixmapItem)

        self.setDragMode(QGraphicsView.DragMode.ScrollHandDrag)
        self.setTransformationAnchor(QGraphicsView.ViewportAnchor.AnchorUnderMouse)
        self.setRenderHint(QPainter.RenderHint.Antialiasing)
        self.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)

    @override
    def wheelEvent(self, event: QWheelEvent):
        # Zoom logic
        zoom_factor = 1.25
        if event.angleDelta().y() > 0:
            self.scale(zoom_factor, zoom_factor)
        else:
            self.scale(1 / zoom_factor, 1 / zoom_factor)
