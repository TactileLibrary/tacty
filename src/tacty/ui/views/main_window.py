from typing import override

from PySide6.QtCore import QByteArray, QSettings
from PySide6.QtGui import QCloseEvent
from PySide6.QtWidgets import QMainWindow


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        settings = QSettings()

        # Set window details.
        self.setWindowTitle
        self.setMinimumSize(800, 450)

        # Restore previous window state.
        settings.beginGroup("window")
        geometry = settings.value("geometry", type=QByteArray)
        if isinstance(geometry, QByteArray):
            _ = self.restoreGeometry(geometry)
        maximized = settings.value("maximized", type=bool)
        if isinstance(maximized, bool) and maximized:
            self.showMaximized()
        settings.endGroup()

    @override
    def closeEvent(self, event: QCloseEvent):
        # Save window state.
        settings = QSettings()
        settings.beginGroup("window")
        settings.setValue("geometry", self.saveGeometry())
        settings.setValue("maximized", self.isMaximized())
        settings.endGroup()

        super().closeEvent(event)
