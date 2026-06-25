from PySide6.QtWidgets import (
    QDialog,
    QDialogButtonBox,
    QFileDialog,
    QFormLayout,
    QLabel,
    QWidget,
)

from tacty.ui.components.path_input import PathInput

from pathlib import Path

class HeatmapDirPickModal(QDialog):
    # Elements
    location: PathInput
    warning: QLabel
    buttonBox: QDialogButtonBox

    valid: bool = False

    def __init__(self, parent: QWidget | None = None):
        super().__init__(parent)

        # Set properties.
        self.setModal(True)
        self.setMinimumWidth(400)
        self.setWindowTitle("Heatmap directory")

        # Add elements.
        layout = QFormLayout()
        self.setLayout(layout)

        title = QLabel("<h2>Pick directory to export heatmaps</h2>")
        layout.addWidget(title)

        self.location = PathInput(
            QFileDialog.AcceptMode.AcceptSave,
            QFileDialog.FileMode.Directory,
            "Location",
            ["All files (*)"],
        )
        _ = self.location.text.textChanged.connect(self.validate)
        layout.addRow("Location", self.location)

        self.warning = QLabel("Warning: Files in the selected directory will be overwritten.")
        self.warning.setWordWrap(True)
        layout.addWidget(self.warning)

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
        self.warning.setText("")

        if not self.location.text.text():
            self.valid = False

        # check if heatmaps already exist in the directory
        mapregex = "heatmap-*.png"

        if self.valid:
            dir_path = Path(self.location.text.text())

            if dir_path.is_dir():
                has_heatmaps = any(dir_path.glob(mapregex))
                if has_heatmaps:
                    # dir, but files already exist
                    # self.valid = False - we can let the user do it, but warn them

                    self.warning.setText(
                        "Warning: Heatmaps already exist in the selected directory and will be overwritten."
                    )

            else:
                # not a dir somehow
                self.valid = False

        if not self.valid:
            self.buttonBox.button(QDialogButtonBox.StandardButton.Ok).setEnabled(False)

    def data(self) -> str:
        return self.location.text.text()