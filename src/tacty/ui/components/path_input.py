from enum import Enum

from PySide6.QtWidgets import QFileDialog, QHBoxLayout, QLineEdit, QPushButton, QWidget


class PathInput(QWidget):
    class FilterType(Enum):
        Text = 1
        Mime = 2

    text: QLineEdit
    title: str
    filters: list[str]
    filterType: FilterType
    mode: QFileDialog.AcceptMode
    # TODO: add a QValidator

    def __init__(
        self,
        mode: QFileDialog.AcceptMode,
        title: str,
        filters: list[str],
        filterType: FilterType = FilterType.Text,
    ):
        super().__init__()

        self.title = title
        self.filters = filters
        self.filterType = filterType
        self.mode = mode

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
        dialog.setAcceptMode(self.mode)

        if self.filterType == PathInput.FilterType.Text:
            dialog.setNameFilters(self.filters)
        else:
            dialog.setMimeTypeFilters(self.filters)

        picked = dialog.exec()
        if picked:
            self.text.setText(dialog.selectedFiles()[0])
