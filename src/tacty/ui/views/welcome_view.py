from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QApplication,
    QLabel,
    QPushButton,
    QStyle,
    QVBoxLayout,
    QWidget,
)


class WelcomeView(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setLayout(layout)

        title = QLabel(f"<h1>{QApplication.applicationDisplayName()}</h1>")
        layout.addWidget(title)

        new_button = QPushButton(
            self.style().standardIcon(QStyle.StandardPixmap.SP_FileDialogNewFolder),
            "New project",
        )
        layout.addWidget(new_button)

        open_button = QPushButton(
            self.style().standardIcon(QStyle.StandardPixmap.SP_DirOpenIcon),
            "Open project",
        )
        layout.addWidget(open_button)

        settings_button = QPushButton(
            "Settings",
        )
        layout.addWidget(settings_button)
