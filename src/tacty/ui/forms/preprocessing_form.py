from PySide6.QtCore import Signal
from PySide6.QtWidgets import QWidget

from tacty.models.project import PreProcessingOptions

from .preprocessing_ui import Ui_Form


class PreProcessingForm(QWidget):
    ui: Ui_Form
    data: PreProcessingOptions
    
    maxFrame: int

    dataChanged: Signal = Signal()

    def __init__(
        self, data: PreProcessingOptions, maxFrame: int
    ):
        super().__init__()

        # load the ui
        self.ui = Ui_Form()
        _ = self.ui.setupUi(self)  # pyright: ignore [reportUnknownMemberType]

        # update the data
        self.data = data
        self.maxFrame = maxFrame
        self.ui.bgrFrame.setMaximum(self.maxFrame)

        self.updateData()
        
        # connectors
        self.ui.bgrEnabled.stateChanged.connect(self.saveData)
        self.ui.bgrFrame.valueChanged.connect(self.saveData)
        self.ui.bgrTolerance.valueChanged.connect(self.saveData)
        self.ui.bgrToleranceSlider.valueChanged.connect(self.saveSlider)


    def updateData(self):
        self.ui.bgrEnabled.setChecked(self.data.bgrEnabled)
        self.ui.bgrFrame.setValue(self.data.bgrFrame)
        self.ui.bgrTolerance.setValue(int(self.data.bgrThreshold * 100))
        self.ui.bgrToleranceSlider.setValue(int(self.data.bgrThreshold * 100))

    def saveData(self):
        self.data.bgrEnabled = self.ui.bgrEnabled.isChecked()
        self.data.bgrFrame = self.ui.bgrFrame.value()
        self.data.bgrThreshold = self.ui.bgrTolerance.value() / 100.0
        self.ui.bgrToleranceSlider.setValue(self.ui.bgrTolerance.value())

        self.dataChanged.emit()

    def saveSlider(self):
        self.ui.bgrTolerance.setValue(self.ui.bgrToleranceSlider.value())
        self.saveData()