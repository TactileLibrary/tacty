from PySide6.QtCore import Signal
from PySide6.QtWidgets import QComboBox, QSlider, QSpinBox, QWidget

from tacty.ui.components.shape_icon import getShapeIcon
from tacty.ui.components.video_player import VideoPlayer
from tacty.ui.models.project import TrackingOptions
from tacty.ui.windows.hue_pick_modal import HuePickModal

from .tracking_ui import Ui_Form


class TrackingForm(QWidget):
    ui: Ui_Form
    data: TrackingOptions
    trackingData: bool

    videoPlayer: VideoPlayer

    startProcessing: Signal = Signal()
    resetTrackingData: Signal = Signal()

    def __init__(
        self, data: TrackingOptions, trackingData: bool, videoPlayer: VideoPlayer
    ):
        super().__init__()

        # load the ui
        self.ui = Ui_Form()
        _ = self.ui.setupUi(self)  # pyright: ignore [reportUnknownMemberType]

        # update the data
        self.trackingData = trackingData
        self.data = data
        self.videoPlayer = videoPlayer

        # connectors
        _ = self.ui.track.clicked.connect(self.startProcessing.emit)
        _ = self.ui.reset.clicked.connect(self.resetTrackingData.emit)

        hue_pairs = {
            "r": self.ui.redHue,
            "y": self.ui.yellowHue,
            "g": self.ui.greenHue,
            "c": self.ui.cyanHue,
            "b": self.ui.blueHue,
            "m": self.ui.magentaHue,
        }

        for key in hue_pairs:
            _ = hue_pairs[key].valueChanged.connect(
                lambda _, h=key, e=hue_pairs[key]: self.syncHue(h, e)  # pyright: ignore [reportUnknownArgumentType, reportUnknownLambdaType]
            )

        hue_button_pairs = {
            self.ui.redHuePick: self.ui.redHue,
            self.ui.yellowHuePick: self.ui.yellowHue,
            self.ui.greenHuePick: self.ui.greenHue,
            self.ui.cyanHuePick: self.ui.cyanHue,
            self.ui.blueHuePick: self.ui.blueHue,
            self.ui.magentaHuePick: self.ui.magentaHue,
        }

        for button in hue_button_pairs:
            _ = button.clicked.connect(
                lambda _, t=hue_button_pairs[button]: self.pickHue(t)  # pyright: ignore [reportUnknownArgumentType, reportUnknownLambdaType]
            )

        tolerance_pairs = [
            ("r", self.ui.redTolerance, self.ui.redToleranceSlider),
            ("y", self.ui.yellowTolerance, self.ui.yellowToleranceSlider),
            ("g", self.ui.greenTolerance, self.ui.greenToleranceSlider),
            ("c", self.ui.cyanTolerance, self.ui.cyanToleranceSlider),
            ("b", self.ui.blueTolerance, self.ui.blueToleranceSlider),
            ("m", self.ui.magentaTolerance, self.ui.magentaToleranceSlider),
        ]

        for color, spin, slider in tolerance_pairs:
            # Use default arguments (a=attr, s=spin, t=slider) to capture
            # the current values in the loop for the lambda closure
            _ = spin.valueChanged.connect(
                lambda _, a=color, s=spin, t=slider: self.syncTolerance(a, s, t)  # pyright: ignore [reportUnknownArgumentType, reportUnknownLambdaType]
            )
            _ = slider.valueChanged.connect(
                lambda _, a=color, s=slider, t=spin: self.syncTolerance(a, s, t)  # pyright: ignore [reportUnknownArgumentType, reportUnknownLambdaType]
            )

        self.initComboBoxes()

        classifier_pairs = [("hu", "Hu Moments"), ("ai", "AI Classifier")]

        for value, text in classifier_pairs:
            self.ui.classifier.addItem(text, value)

        _ = self.ui.classifier.currentIndexChanged.connect(self.updateClassifier)

        self.updateData()

    def updateClassifier(self) -> None:
        data: str = self.ui.classifier.currentData()  # pyright: ignore [reportAny]
        self.data.classifier = data

    def initComboBoxes(self) -> None:
        boxes = [
            (self.ui.leftThumb, "leftThumb"),
            (self.ui.leftIndex, "leftIndex"),
            (self.ui.leftMiddle, "leftMiddle"),
            (self.ui.leftRing, "leftRing"),
            (self.ui.leftPinky, "leftPinky"),
            (self.ui.leftPalm, "leftPalm"),
            (self.ui.rightThumb, "rightThumb"),
            (self.ui.rightIndex, "rightIndex"),
            (self.ui.rightMiddle, "rightMiddle"),
            (self.ui.rightRing, "rightRing"),
            (self.ui.rightPinky, "rightPinky"),
            (self.ui.rightPalm, "rightPalm"),
        ]

        for box, finger in boxes:
            self.addBoxOptions(box, finger)

    def addBoxOptions(self, box: QComboBox, finger: str):
        colors = ["red", "yellow", "green", "cyan", "blue", "magenta"]
        shapes = ["circle", "square"]

        combinations = [(c, s) for c in colors for s in shapes]

        for color, shape in combinations:
            name = color.capitalize() + " " + shape
            value = color + shape.capitalize()
            icon = getShapeIcon(color=color, shape=shape)

            box.addItem(icon, name, value)

        _ = box.currentIndexChanged.connect(
            lambda _, b=box, f=finger: self.saveComboBox(b, f)  # pyright: ignore [reportUnknownArgumentType, reportUnknownLambdaType]
        )

    def setComboBoxToData(self, box: QComboBox, data: str):
        index = box.findData(data)
        box.setCurrentIndex(index)

    def updateComboBoxes(self):
        self.setComboBoxToData(self.ui.leftThumb, self.data.fingerMapping.leftThumb)
        self.setComboBoxToData(self.ui.leftIndex, self.data.fingerMapping.leftIndex)
        self.setComboBoxToData(self.ui.leftMiddle, self.data.fingerMapping.leftMiddle)
        self.setComboBoxToData(self.ui.leftRing, self.data.fingerMapping.leftRing)
        self.setComboBoxToData(self.ui.leftPinky, self.data.fingerMapping.leftPinky)
        self.setComboBoxToData(self.ui.leftPalm, self.data.fingerMapping.leftPalm)
        self.setComboBoxToData(self.ui.rightThumb, self.data.fingerMapping.rightThumb)
        self.setComboBoxToData(self.ui.rightIndex, self.data.fingerMapping.rightIndex)
        self.setComboBoxToData(self.ui.rightMiddle, self.data.fingerMapping.rightMiddle)
        self.setComboBoxToData(self.ui.rightRing, self.data.fingerMapping.rightRing)
        self.setComboBoxToData(self.ui.rightPinky, self.data.fingerMapping.rightPinky)
        self.setComboBoxToData(self.ui.rightPalm, self.data.fingerMapping.rightPalm)

    def saveComboBox(self, box: QComboBox, finger: str):
        setattr(self.data.fingerMapping, finger, box.currentData())

    def syncHue(self, key: str, element: QSpinBox):
        setattr(self.data.hues, key, element.value())

    def pickHue(self, target: QSpinBox):
        img = self.videoPlayer.getPixmap()
        if img is None:
            return
        hue = HuePickModal.pickHue(img)
        if hue:
            target.setValue(hue)

    def updateData(self):
        # hues
        self.ui.redHue.setValue(self.data.hues.r)
        self.ui.yellowHue.setValue(self.data.hues.y)
        self.ui.greenHue.setValue(self.data.hues.g)
        self.ui.cyanHue.setValue(self.data.hues.c)
        self.ui.blueHue.setValue(self.data.hues.b)
        self.ui.magentaHue.setValue(self.data.hues.m)

        # tolerances
        self.ui.redTolerance.setValue(int(self.data.tolerances.r * 100))
        self.ui.yellowTolerance.setValue(int(self.data.tolerances.y * 100))
        self.ui.greenTolerance.setValue(int(self.data.tolerances.g * 100))
        self.ui.cyanTolerance.setValue(int(self.data.tolerances.c * 100))
        self.ui.blueTolerance.setValue(int(self.data.tolerances.b * 100))
        self.ui.magentaTolerance.setValue(int(self.data.tolerances.m * 100))

        # buttons
        self.ui.reset.setDisabled(True)
        if self.trackingData:
            self.ui.reset.setDisabled(False)

        # combo boxes
        self.updateComboBoxes()

        # classifier
        index = self.ui.classifier.findData(self.data.classifier)
        self.ui.classifier.setCurrentIndex(index)

    def syncTolerance(
        self, color: str, source: QSpinBox | QSlider, target: QSpinBox | QSlider
    ):
        val = source.value()

        # Update the data model
        setattr(self.data.tolerances, color, val / 100.0)

        # Update the "buddy" widget without triggering its signal
        _ = target.blockSignals(True)
        target.setValue(val)
        _ = target.blockSignals(False)
