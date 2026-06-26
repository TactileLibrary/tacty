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
        _ = self.ui.bgrEnabled.stateChanged.connect(self.saveBGR)
        _ = self.ui.bgrEnabled.stateChanged.connect(self.EnableDisableControls)
        _ = self.ui.bgrFrame.valueChanged.connect(self.saveBGR)
        _ = self.ui.bgrTolerance.valueChanged.connect(self.saveBGR)
        _ = self.ui.bgrToleranceSlider.valueChanged.connect(self.saveBGRSlider)

        _ = self.ui.denoisingEnabled.stateChanged.connect(self.saveDenoising)
        _ = self.ui.denoisingEnabled.stateChanged.connect(self.EnableDisableControls)
        _ = self.ui.denoisingSize.valueChanged.connect(self.saveDenoising)
        _ = self.ui.denoisingSizeSlider.valueChanged.connect(self.saveDenoisingSlider)
        _ = self.ui.denoisingFilter.currentTextChanged.connect(self.saveDenoising)


    def updateData(self):
        # bgr
        self.ui.bgrEnabled.setChecked(self.data.bgrEnabled)
        self.ui.bgrFrame.setValue(self.data.bgrFrame)
        self.ui.bgrTolerance.setValue(int(self.data.bgrThreshold * 100))
        self.ui.bgrToleranceSlider.setValue(int(self.data.bgrThreshold * 100))

        # denoising
        self.ui.denoisingEnabled.setChecked(self.data.denoiseEnabled)
        self.ui.denoisingSize.setValue(self.data.denoiseSize)
        self.ui.denoisingFilter.setCurrentText(self.data.denoiseFilter.capitalize())
        self.ui.denoisingSizeSlider.setValue(self.data.denoiseSize)

        # states
        self.EnableDisableControls()

    def saveBGR(self):
        self.data.bgrEnabled = self.ui.bgrEnabled.isChecked()
        self.data.bgrFrame = self.ui.bgrFrame.value()
        self.data.bgrThreshold = self.ui.bgrTolerance.value() / 100.0
        self.ui.bgrToleranceSlider.setValue(self.ui.bgrTolerance.value())

        self.dataChanged.emit()

    def saveBGRSlider(self):
        self.ui.bgrTolerance.setValue(self.ui.bgrToleranceSlider.value())
        self.saveBGR()

    def saveDenoising(self):
        self.data.denoiseEnabled = self.ui.denoisingEnabled.isChecked()
        self.data.denoiseFilter = self.ui.denoisingFilter.currentText().lower()
        
        # denoising size must be odd
        size = self.ui.denoisingSize.value()
        if size % 2 == 0:
            size += 1
            self.ui.denoisingSize.blockSignals(True)
            self.ui.denoisingSize.setValue(size)
            self.ui.denoisingSize.blockSignals(False)
        self.data.denoiseSize = size
        self.ui.denoisingSizeSlider.blockSignals(True)
        self.ui.denoisingSizeSlider.setValue(size)
        self.ui.denoisingSizeSlider.blockSignals(False)

        self.dataChanged.emit()

    def saveDenoisingSlider(self):
        self.ui.denoisingSize.setValue(self.ui.denoisingSizeSlider.value())

    def EnableDisableControls(self):
        bgrEnabled = self.ui.bgrEnabled.isChecked()
        self.ui.bgrFrame.setEnabled(bgrEnabled)
        self.ui.bgrTolerance.setEnabled(bgrEnabled)
        self.ui.bgrToleranceSlider.setEnabled(bgrEnabled)

        denoiseEnabled = self.ui.denoisingEnabled.isChecked()
        self.ui.denoisingSize.setEnabled(denoiseEnabled)
        self.ui.denoisingSizeSlider.setEnabled(denoiseEnabled)
        self.ui.denoisingFilter.setEnabled(denoiseEnabled)