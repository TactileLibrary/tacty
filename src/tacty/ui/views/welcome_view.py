from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QApplication,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QWidget,
)


class WelcomeView(QWidget):
    # Signals
    openProject: Signal = Signal()
    newProject: Signal = Signal()

    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setLayout(layout)

        title = QLabel(f"<h1>{QApplication.applicationDisplayName()}</h1>")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        newButton = QPushButton("New project")
        _ = newButton.clicked.connect(self.newProject.emit)
        layout.addWidget(newButton)

        openButton = QPushButton("Open project")
        _ = openButton.clicked.connect(self.openProject.emit)
        layout.addWidget(openButton)
