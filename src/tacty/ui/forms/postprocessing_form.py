from PySide6.QtCore import Signal
from PySide6.QtWidgets import QWidget

from tacty.models.project import PostProcessingOptions

from .postprocessing_ui import Ui_Form


class PostProcessingForm(QWidget):
    ui: Ui_Form

    data: PostProcessingOptions

    dataChanged: Signal = Signal()

    def __init__(self, data: PostProcessingOptions):
        super().__init__()

        # load the ui
        self.ui = Ui_Form()
        _ = self.ui.setupUi(self)  # pyright: ignore [reportUnknownMemberType]

        self.data = data
        self.updateData()

        # connectors
        _ = self.ui.outlierAnatomy.checkStateChanged.connect(self.saveData)
        _ = self.ui.outlierSpeed.checkStateChanged.connect(self.saveData)
        _ = self.ui.interpolation.checkStateChanged.connect(self.saveData)

    def updateData(self):
        self.ui.outlierAnatomy.setChecked(self.data.anatomyOutlier)
        self.ui.outlierSpeed.setChecked(self.data.speedOutlier)
        self.ui.interpolation.setChecked(self.data.interpolation)

    def saveData(self):
        self.data.anatomyOutlier = self.ui.outlierAnatomy.isChecked()
        self.data.speedOutlier = self.ui.outlierSpeed.isChecked()
        self.data.interpolation = self.ui.interpolation.isChecked()

        self.dataChanged.emit()
