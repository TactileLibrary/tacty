# pyright: reportUnknownMemberType=false
# because pandas

from typing import cast

import numpy as np
import pandas as pd
from PySide6.QtCore import QFileInfo, QSettings
from PySide6.QtWidgets import QFileDialog, QWidget

from .export_ui import Ui_Form


class ExportForm(QWidget):
    ui: Ui_Form

    data: pd.DataFrame | None = None

    fps: float | None = None
    name: str | None = None

    def __init__(self):
        super().__init__()

        # load the ui
        self.ui = Ui_Form()
        _ = self.ui.setupUi(self)

        self.updateData()  # disables the buttons

        # connectors
        _ = self.ui.flatCSV.clicked.connect(self.saveToCSV)
        _ = self.ui.flatXLSX.clicked.connect(self.saveToXLSX)
        _ = self.ui.gazePlotter.clicked.connect(self.saveToGazePlotter)

    def updateData(
        self,
        data: pd.DataFrame | None = None,
        fps: float | None = None,
        name: str | None = None,
    ):
        self.data = data
        self.fps = fps
        self.name = name

        buttons = [self.ui.flatCSV, self.ui.flatXLSX, self.ui.gazePlotter]
        enabled = self.data is not None and fps is not None and name is not None

        for button in buttons:
            button.setEnabled(enabled)

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
            folder = QFileInfo(fileName).absolutePath()
            settings.setValue("lastPath", folder)
            return fileName
        return None

    def filterData(self) -> pd.DataFrame | None:
        if self.data is None or self.fps is None:
            return None

        filtered: pd.DataFrame = cast(
            pd.DataFrame,
            self.data.loc[
                :, ~self.data.columns.get_level_values(1).str.startswith("_")
            ].copy(),
        )

        mpf = 1000 / self.fps

        filtered.index = (filtered.index * mpf).round().astype(int)

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

    def saveToGazePlotter(self):
        data = self.filterData()
        if data is None:
            return

        # reshape the data into the GazePlotter requirements
        data.index.name = "Time"

        stacked = data.stack(level=0)
        stacked = stacked.reset_index()
        stacked.rename(columns={"level_1": "Participant"}, inplace=True)

        # identify AOI columns
        aoi_cols = [col for col in stacked.columns if str(col).startswith("in_")]
        aoi_names = [col.replace("in_", "") for col in aoi_cols]

        def joinAOIs(row) -> str:
            active_aois = [aoi_names[i] for i, val in enumerate(row) if val == 1]
            return "|".join(active_aois) if active_aois else ""

        aoi_strings = stacked[aoi_cols].apply(joinAOIs, axis=1)

        # assemble the final df
        export = pd.DataFrame(
            {
                "Time": stacked["Time"].astype(int),
                "Participant": stacked["Participant"].astype(str),
                "Stimulus": self.name,
                "AOI": aoi_strings,
                "X": stacked["x"] if "x" in stacked.columns else np.nan,
                "Y": stacked["y"] if "y" in stacked.columns else np.nan,
            }
        )

        export.sort_values(by=["Participant", "Time"], inplace=True)

        # save to disk
        loc = self.getSaveLocation("csv")
        if loc is None:
            return
        export.to_csv(loc, index=False)
