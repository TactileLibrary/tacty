# pyright: reportUnknownMemberType=false
# because pandas

from typing import cast

import pandas as pd
from PySide6.QtCore import QFileInfo, QSettings
from PySide6.QtWidgets import QFileDialog, QWidget

from .export_ui import Ui_Form


class ExportForm(QWidget):
    ui: Ui_Form

    data: pd.DataFrame | None = None

    def __init__(self):
        super().__init__()

        # load the ui
        self.ui = Ui_Form()
        _ = self.ui.setupUi(self)

        self.updateData()  # disables the buttons

        # connectors
        _ = self.ui.positionCSV.clicked.connect(self.saveToCSV)
        _ = self.ui.positionXLSX.clicked.connect(self.saveToXLSX)

    def updateData(self, data: pd.DataFrame | None = None):
        self.data = data

        self.ui.positionCSV.setDisabled(True)
        self.ui.positionXLSX.setDisabled(True)
        if self.data is not None:
            self.ui.positionCSV.setDisabled(False)
            self.ui.positionXLSX.setDisabled(False)

    def getSaveLocation(self, ext: str) -> str | None:
        dialog = QFileDialog(self)

        dialog.setWindowTitle(f"Save to {ext}")
        dialog.setAcceptMode(QFileDialog.AcceptMode.AcceptSave)
        dialog.setNameFilter(f"*.{ext}")

        settings = QSettings()
        defaultPath = settings.value("lastPath", type=str)
        if not isinstance(defaultPath, str):
            defaultPath = ""

        dialog.setDirectory(defaultPath)

        picked = dialog.exec()
        if picked:
            fileName = dialog.selectedFiles()[0]
            folder = QFileInfo(fileName).canonicalPath()
            settings.setValue("lastPath", folder)
            return fileName
        return None

    def filterData(self) -> pd.DataFrame | None:
        if self.data is None:
            return None

        filtered: pd.DataFrame = cast(
            pd.DataFrame,
            self.data.loc[
                :, ~self.data.columns.get_level_values(1).str.startswith("_")
            ].copy(),
        )

        return filtered

    def saveToCSV(self):
        data = self.filterData()
        if data is None:
            return
        loc = self.getSaveLocation("csv")
        if loc is None:
            return
        data.to_csv(loc)

    def saveToXLSX(self):
        data = self.filterData()
        if data is None:
            return
        loc = self.getSaveLocation("xlsx")
        if loc is None:
            return
        data.to_excel(loc)
