from PySide6.QtCore import Signal
from PySide6.QtWidgets import (
    QAbstractItemView,
    QHeaderView,
    QMessageBox,
    QTableWidgetItem,
    QWidget,
)

from tacty.models.project import AOIRect, Point, PostProcessingOptions
from tacty.ui.windows.validated_text_modal import ValidatedInputDialog
from tacty.utils.AOIValidator import AOINameValidator

from .postprocessing_ui import Ui_Form


class PostProcessingForm(QWidget):
    ui: Ui_Form

    data: PostProcessingOptions

    selectedAOI: int = -1

    dataChanged: Signal = Signal()
    requestRect: Signal = Signal()

    def __init__(self, data: PostProcessingOptions):
        super().__init__()

        # load the ui
        self.ui = Ui_Form()
        _ = self.ui.setupUi(self)  # pyright: ignore [reportUnknownMemberType]

        self.data = data
        self.updateData()
        self.updateTable()
        self.toggleDelButton()

        # connectors
        _ = self.ui.outlierAnatomy.checkStateChanged.connect(self.saveData)
        _ = self.ui.outlierSpeed.checkStateChanged.connect(self.saveData)
        _ = self.ui.interpolation.checkStateChanged.connect(self.saveData)
        _ = self.ui.AOIAddRect.clicked.connect(self.requestRect.emit)
        _ = self.ui.AOITable.itemSelectionChanged.connect(self.toggleDelButton)
        _ = self.ui.AOIDelete.clicked.connect(self.deleteAOI)

        # disable poly since it's not implemented yet
        self.ui.AOIAddPoly.setDisabled(True)

    def deleteAOI(self):
        if self.selectedAOI == -1:
            return

        name = self.data.aois[self.selectedAOI].name
        confirm = QMessageBox.question(
            self,
            "Confirm AOI deletion",
            f"Are you sure you want to delete '{name}'?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No,
        )

        if confirm == QMessageBox.StandardButton.Yes:
            _ = self.data.aois.pop(self.selectedAOI)
            self.updateTable()

    def toggleDelButton(self):
        self.selectedAOI = self.ui.AOITable.currentRow()
        self.ui.AOIDelete.setEnabled(len(self.ui.AOITable.selectedItems()) > 0)

    def updateData(self):
        self.ui.outlierAnatomy.setChecked(self.data.anatomyOutlier)
        self.ui.outlierSpeed.setChecked(self.data.speedOutlier)
        self.ui.interpolation.setChecked(self.data.interpolation)

    def saveData(self):
        self.data.anatomyOutlier = self.ui.outlierAnatomy.isChecked()
        self.data.speedOutlier = self.ui.outlierSpeed.isChecked()
        self.data.interpolation = self.ui.interpolation.isChecked()

        self.dataChanged.emit()

    def updateTable(self):
        # clear previous data
        self.ui.AOITable.clearContents()

        # set up properties
        self.ui.AOITable.setColumnCount(2)
        self.ui.AOITable.setRowCount(len(self.data.aois))
        self.ui.AOITable.setHorizontalHeaderLabels(["Name", "Type"])
        self.ui.AOITable.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.ui.AOITable.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch
        )
        self.ui.AOITable.setSelectionBehavior(
            QAbstractItemView.SelectionBehavior.SelectRows
        )

        # populate
        for idx, aoi in enumerate(self.data.aois):
            self.ui.AOITable.setItem(idx, 0, QTableWidgetItem(aoi.name))
            self.ui.AOITable.setItem(idx, 1, QTableWidgetItem(aoi.type.value))

    def addRectangleAOI(self, tl: Point, br: Point):
        # get name
        used = [aoi.name for aoi in self.data.aois]

        validator = AOINameValidator(used)

        name = ValidatedInputDialog.getText(title="AOI Name", validator=validator)

        if not name:
            return

        aoi = AOIRect(name=name, tl=tl, br=br)
        self.data.aois.append(aoi)

        self.updateTable()
        self.dataChanged.emit()
