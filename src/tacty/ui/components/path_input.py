from enum import Enum

from PySide6.QtCore import QFileInfo, QSettings, QStandardPaths
from PySide6.QtWidgets import QFileDialog, QHBoxLayout, QLineEdit, QPushButton, QWidget


class PathInput(QWidget):
    class FilterType(Enum):
        Text = 1
        Mime = 2

    text: QLineEdit
    title: str
    filters: list[str]
    filterType: FilterType
    acceptMode: QFileDialog.AcceptMode
    fileMode: QFileDialog.FileMode
    # TODO: add a QValidator

    def __init__(
        self,
        acceptMode: QFileDialog.AcceptMode,
        fileMode: QFileDialog.FileMode,
        title: str,
        filters: list[str],
        filterType: FilterType = FilterType.Text,
    ):
        super().__init__()

        self.title = title
        self.filters = filters
        self.filterType = filterType
        self.acceptMode = acceptMode
        self.fileMode = fileMode
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)

        self.text = QLineEdit()
        layout.addWidget(self.text)

        button = QPushButton("Browse")
        _ = button.clicked.connect(self.openPicker)
        layout.addWidget(button)

    def openPicker(self):
        dialog = QFileDialog(self)

        dialog.setWindowTitle(self.title)
        dialog.setAcceptMode(self.acceptMode)
        dialog.setFileMode(self.fileMode)

        if self.filterType == PathInput.FilterType.Text:
            dialog.setNameFilters(self.filters)
        else:
            dialog.setMimeTypeFilters(self.filters)

        settings = QSettings()
        defaultPath = settings.value("lastPath", type=str)
        if not isinstance(defaultPath, str):
            defaultPath = QStandardPaths.writableLocation(
                QStandardPaths.StandardLocation.DocumentsLocation
            )

        dialog.setDirectory(defaultPath)

        picked = dialog.exec()
        if picked:
            fileName = dialog.selectedFiles()[0]
            self.text.setText(fileName)
            folder = QFileInfo(fileName).absolutePath()
            settings.setValue("lastPath", folder)
