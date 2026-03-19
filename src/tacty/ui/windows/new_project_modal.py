from PySide6.QtCore import QMimeDatabase, QMimeType
from PySide6.QtWidgets import (
    QDialog,
    QDialogButtonBox,
    QFileDialog,
    QFormLayout,
    QLabel,
)

from tacty.ui.components.path_input import PathInput


class NewProjectModal(QDialog):
    # Elements
    projectLocation: PathInput
    videoLocation: PathInput
    buttonBox: QDialogButtonBox

    valid: bool = False

    def __init__(self):
        super().__init__()

        # Set properties.
        self.setModal(True)
        self.setMinimumWidth(400)
        self.setWindowTitle("New project")

        # Add elements.
        layout = QFormLayout()
        self.setLayout(layout)

        title = QLabel("<h2>Create a new project</h2>")
        layout.addWidget(title)

        self.projectLocation = PathInput(
            QFileDialog.AcceptMode.AcceptSave,
            "Project location",
            ["Tacty Project (*.tproj)"],
        )
        _ = self.projectLocation.text.textChanged.connect(self.validate)
        layout.addRow("Project location", self.projectLocation)

        self.videoLocation = PathInput(
            QFileDialog.AcceptMode.AcceptOpen,
            "Video location",
            ["Video files (*.mov *.mp4 *.avi *.webm *.mkv)"],
        )
        _ = self.videoLocation.text.textChanged.connect(self.validate)
        layout.addRow("Video file", self.videoLocation)

        self.buttonBox = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel,
            self,
        )
        self.buttonBox.button(QDialogButtonBox.StandardButton.Ok).setDefault(True)

        _ = self.buttonBox.accepted.connect(self.accept)
        _ = self.buttonBox.rejected.connect(self.reject)

        layout.addWidget(self.buttonBox)

        self.validate()

    def validate(self):
        self.valid = True
        self.buttonBox.button(QDialogButtonBox.StandardButton.Ok).setEnabled(True)

        if not self.projectLocation.text.text():
            self.valid = False

        if not self.videoLocation.text.text():
            self.valid = False

        if not self.valid:
            self.buttonBox.button(QDialogButtonBox.StandardButton.Ok).setEnabled(False)

    def data(self) -> tuple[str, str]:
        return self.projectLocation.text.text(), self.videoLocation.text.text()
