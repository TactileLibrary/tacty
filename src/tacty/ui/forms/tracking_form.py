from PySide6.QtCore import Signal
from PySide6.QtWidgets import QWidget

from .tracking_ui import Ui_Form


class TrackingForm(QWidget):
    ui: Ui_Form

    startProcessing: Signal = Signal()

    def __init__(self):
        super().__init__()

        # load the ui
        self.ui = Ui_Form()
        _ = self.ui.setupUi(self)  # pyright: ignore [reportUnknownMemberType]

        # update the data
        # for now no data

        # connectors
        _ = self.ui.track.clicked.connect(self.startProcessing.emit)
