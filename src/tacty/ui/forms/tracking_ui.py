# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'tracking.ui'
##
## Created by: Qt User Interface Compiler version 6.10.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QComboBox, QFormLayout, QHBoxLayout,
    QLabel, QPushButton, QSizePolicy, QSlider,
    QSpacerItem, QSpinBox, QVBoxLayout, QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(501, 873)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Form.sizePolicy().hasHeightForWidth())
        Form.setSizePolicy(sizePolicy)
        self.verticalLayout = QVBoxLayout(Form)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.trackerMappingLabel = QLabel(Form)
        self.trackerMappingLabel.setObjectName(u"trackerMappingLabel")
        self.trackerMappingLabel.setTextFormat(Qt.TextFormat.MarkdownText)

        self.verticalLayout.addWidget(self.trackerMappingLabel)

        self.horizontalLayout_13 = QHBoxLayout()
        self.horizontalLayout_13.setObjectName(u"horizontalLayout_13")
        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.leftHandLabel = QLabel(Form)
        self.leftHandLabel.setObjectName(u"leftHandLabel")
        self.leftHandLabel.setTextFormat(Qt.TextFormat.PlainText)

        self.verticalLayout_3.addWidget(self.leftHandLabel)

        self.formLayout = QFormLayout()
        self.formLayout.setObjectName(u"formLayout")
        self.leftThumb = QComboBox(Form)
        self.leftThumb.setObjectName(u"leftThumb")

        self.formLayout.setWidget(0, QFormLayout.ItemRole.FieldRole, self.leftThumb)

        self.leftIndexLabel = QLabel(Form)
        self.leftIndexLabel.setObjectName(u"leftIndexLabel")

        self.formLayout.setWidget(1, QFormLayout.ItemRole.LabelRole, self.leftIndexLabel)

        self.leftIndex = QComboBox(Form)
        self.leftIndex.setObjectName(u"leftIndex")

        self.formLayout.setWidget(1, QFormLayout.ItemRole.FieldRole, self.leftIndex)

        self.leftMiddleLabel = QLabel(Form)
        self.leftMiddleLabel.setObjectName(u"leftMiddleLabel")

        self.formLayout.setWidget(2, QFormLayout.ItemRole.LabelRole, self.leftMiddleLabel)

        self.leftMiddle = QComboBox(Form)
        self.leftMiddle.setObjectName(u"leftMiddle")

        self.formLayout.setWidget(2, QFormLayout.ItemRole.FieldRole, self.leftMiddle)

        self.leftRingLabel = QLabel(Form)
        self.leftRingLabel.setObjectName(u"leftRingLabel")

        self.formLayout.setWidget(3, QFormLayout.ItemRole.LabelRole, self.leftRingLabel)

        self.leftRing = QComboBox(Form)
        self.leftRing.setObjectName(u"leftRing")

        self.formLayout.setWidget(3, QFormLayout.ItemRole.FieldRole, self.leftRing)

        self.leftPinkyLabel = QLabel(Form)
        self.leftPinkyLabel.setObjectName(u"leftPinkyLabel")

        self.formLayout.setWidget(4, QFormLayout.ItemRole.LabelRole, self.leftPinkyLabel)

        self.leftPinky = QComboBox(Form)
        self.leftPinky.setObjectName(u"leftPinky")

        self.formLayout.setWidget(4, QFormLayout.ItemRole.FieldRole, self.leftPinky)

        self.leftPalmLabel = QLabel(Form)
        self.leftPalmLabel.setObjectName(u"leftPalmLabel")

        self.formLayout.setWidget(5, QFormLayout.ItemRole.LabelRole, self.leftPalmLabel)

        self.leftPalm = QComboBox(Form)
        self.leftPalm.setObjectName(u"leftPalm")

        self.formLayout.setWidget(5, QFormLayout.ItemRole.FieldRole, self.leftPalm)

        self.leftThumbLabel = QLabel(Form)
        self.leftThumbLabel.setObjectName(u"leftThumbLabel")

        self.formLayout.setWidget(0, QFormLayout.ItemRole.LabelRole, self.leftThumbLabel)


        self.verticalLayout_3.addLayout(self.formLayout)


        self.horizontalLayout_13.addLayout(self.verticalLayout_3)

        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.rightHandLabel = QLabel(Form)
        self.rightHandLabel.setObjectName(u"rightHandLabel")
        self.rightHandLabel.setTextFormat(Qt.TextFormat.PlainText)

        self.verticalLayout_2.addWidget(self.rightHandLabel)

        self.formLayout_3 = QFormLayout()
        self.formLayout_3.setObjectName(u"formLayout_3")
        self.rightThumb = QComboBox(Form)
        self.rightThumb.setObjectName(u"rightThumb")

        self.formLayout_3.setWidget(0, QFormLayout.ItemRole.FieldRole, self.rightThumb)

        self.rightIndexLabel = QLabel(Form)
        self.rightIndexLabel.setObjectName(u"rightIndexLabel")

        self.formLayout_3.setWidget(1, QFormLayout.ItemRole.LabelRole, self.rightIndexLabel)

        self.rightIndex = QComboBox(Form)
        self.rightIndex.setObjectName(u"rightIndex")

        self.formLayout_3.setWidget(1, QFormLayout.ItemRole.FieldRole, self.rightIndex)

        self.rightMiddleLabel = QLabel(Form)
        self.rightMiddleLabel.setObjectName(u"rightMiddleLabel")

        self.formLayout_3.setWidget(2, QFormLayout.ItemRole.LabelRole, self.rightMiddleLabel)

        self.rightMiddle = QComboBox(Form)
        self.rightMiddle.setObjectName(u"rightMiddle")

        self.formLayout_3.setWidget(2, QFormLayout.ItemRole.FieldRole, self.rightMiddle)

        self.rightRingLabel = QLabel(Form)
        self.rightRingLabel.setObjectName(u"rightRingLabel")

        self.formLayout_3.setWidget(3, QFormLayout.ItemRole.LabelRole, self.rightRingLabel)

        self.rightRing = QComboBox(Form)
        self.rightRing.setObjectName(u"rightRing")

        self.formLayout_3.setWidget(3, QFormLayout.ItemRole.FieldRole, self.rightRing)

        self.rightPinkyLabel = QLabel(Form)
        self.rightPinkyLabel.setObjectName(u"rightPinkyLabel")

        self.formLayout_3.setWidget(4, QFormLayout.ItemRole.LabelRole, self.rightPinkyLabel)

        self.rightPinky = QComboBox(Form)
        self.rightPinky.setObjectName(u"rightPinky")

        self.formLayout_3.setWidget(4, QFormLayout.ItemRole.FieldRole, self.rightPinky)

        self.rightPalmLabel = QLabel(Form)
        self.rightPalmLabel.setObjectName(u"rightPalmLabel")

        self.formLayout_3.setWidget(5, QFormLayout.ItemRole.LabelRole, self.rightPalmLabel)

        self.rightPalm = QComboBox(Form)
        self.rightPalm.setObjectName(u"rightPalm")

        self.formLayout_3.setWidget(5, QFormLayout.ItemRole.FieldRole, self.rightPalm)

        self.rightThumbLabel = QLabel(Form)
        self.rightThumbLabel.setObjectName(u"rightThumbLabel")

        self.formLayout_3.setWidget(0, QFormLayout.ItemRole.LabelRole, self.rightThumbLabel)


        self.verticalLayout_2.addLayout(self.formLayout_3)


        self.horizontalLayout_13.addLayout(self.verticalLayout_2)


        self.verticalLayout.addLayout(self.horizontalLayout_13)

        self.colorHuesLabel = QLabel(Form)
        self.colorHuesLabel.setObjectName(u"colorHuesLabel")
        self.colorHuesLabel.setTextFormat(Qt.TextFormat.MarkdownText)

        self.verticalLayout.addWidget(self.colorHuesLabel)

        self.colorForm = QFormLayout()
        self.colorForm.setObjectName(u"colorForm")
        self.redHueLabel = QLabel(Form)
        self.redHueLabel.setObjectName(u"redHueLabel")

        self.colorForm.setWidget(0, QFormLayout.ItemRole.LabelRole, self.redHueLabel)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.redHue = QSpinBox(Form)
        self.redHue.setObjectName(u"redHue")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.redHue.sizePolicy().hasHeightForWidth())
        self.redHue.setSizePolicy(sizePolicy1)
        self.redHue.setMaximum(179)

        self.horizontalLayout.addWidget(self.redHue)

        self.redHuePick = QPushButton(Form)
        self.redHuePick.setObjectName(u"redHuePick")

        self.horizontalLayout.addWidget(self.redHuePick)


        self.colorForm.setLayout(0, QFormLayout.ItemRole.FieldRole, self.horizontalLayout)

        self.yellowHueLabel = QLabel(Form)
        self.yellowHueLabel.setObjectName(u"yellowHueLabel")

        self.colorForm.setWidget(1, QFormLayout.ItemRole.LabelRole, self.yellowHueLabel)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.yellowHue = QSpinBox(Form)
        self.yellowHue.setObjectName(u"yellowHue")
        sizePolicy1.setHeightForWidth(self.yellowHue.sizePolicy().hasHeightForWidth())
        self.yellowHue.setSizePolicy(sizePolicy1)
        self.yellowHue.setMaximum(179)

        self.horizontalLayout_2.addWidget(self.yellowHue)

        self.yellowHuePick = QPushButton(Form)
        self.yellowHuePick.setObjectName(u"yellowHuePick")

        self.horizontalLayout_2.addWidget(self.yellowHuePick)


        self.colorForm.setLayout(1, QFormLayout.ItemRole.FieldRole, self.horizontalLayout_2)

        self.greenHueLabel = QLabel(Form)
        self.greenHueLabel.setObjectName(u"greenHueLabel")

        self.colorForm.setWidget(2, QFormLayout.ItemRole.LabelRole, self.greenHueLabel)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.greenHue = QSpinBox(Form)
        self.greenHue.setObjectName(u"greenHue")
        sizePolicy1.setHeightForWidth(self.greenHue.sizePolicy().hasHeightForWidth())
        self.greenHue.setSizePolicy(sizePolicy1)
        self.greenHue.setMaximum(179)

        self.horizontalLayout_3.addWidget(self.greenHue)

        self.greenHuePick = QPushButton(Form)
        self.greenHuePick.setObjectName(u"greenHuePick")

        self.horizontalLayout_3.addWidget(self.greenHuePick)


        self.colorForm.setLayout(2, QFormLayout.ItemRole.FieldRole, self.horizontalLayout_3)

        self.cyanHueLabel = QLabel(Form)
        self.cyanHueLabel.setObjectName(u"cyanHueLabel")

        self.colorForm.setWidget(3, QFormLayout.ItemRole.LabelRole, self.cyanHueLabel)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.cyanHue = QSpinBox(Form)
        self.cyanHue.setObjectName(u"cyanHue")
        sizePolicy1.setHeightForWidth(self.cyanHue.sizePolicy().hasHeightForWidth())
        self.cyanHue.setSizePolicy(sizePolicy1)
        self.cyanHue.setMaximum(179)

        self.horizontalLayout_4.addWidget(self.cyanHue)

        self.cyanHuePick = QPushButton(Form)
        self.cyanHuePick.setObjectName(u"cyanHuePick")

        self.horizontalLayout_4.addWidget(self.cyanHuePick)


        self.colorForm.setLayout(3, QFormLayout.ItemRole.FieldRole, self.horizontalLayout_4)

        self.blueHueLabel = QLabel(Form)
        self.blueHueLabel.setObjectName(u"blueHueLabel")

        self.colorForm.setWidget(4, QFormLayout.ItemRole.LabelRole, self.blueHueLabel)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.blueHue = QSpinBox(Form)
        self.blueHue.setObjectName(u"blueHue")
        sizePolicy1.setHeightForWidth(self.blueHue.sizePolicy().hasHeightForWidth())
        self.blueHue.setSizePolicy(sizePolicy1)
        self.blueHue.setMaximum(179)

        self.horizontalLayout_5.addWidget(self.blueHue)

        self.blueHuePick = QPushButton(Form)
        self.blueHuePick.setObjectName(u"blueHuePick")

        self.horizontalLayout_5.addWidget(self.blueHuePick)


        self.colorForm.setLayout(4, QFormLayout.ItemRole.FieldRole, self.horizontalLayout_5)

        self.magentaHueLabel = QLabel(Form)
        self.magentaHueLabel.setObjectName(u"magentaHueLabel")

        self.colorForm.setWidget(5, QFormLayout.ItemRole.LabelRole, self.magentaHueLabel)

        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.magentaHue = QSpinBox(Form)
        self.magentaHue.setObjectName(u"magentaHue")
        sizePolicy1.setHeightForWidth(self.magentaHue.sizePolicy().hasHeightForWidth())
        self.magentaHue.setSizePolicy(sizePolicy1)
        self.magentaHue.setMaximum(179)

        self.horizontalLayout_6.addWidget(self.magentaHue)

        self.magentaHuePick = QPushButton(Form)
        self.magentaHuePick.setObjectName(u"magentaHuePick")

        self.horizontalLayout_6.addWidget(self.magentaHuePick)


        self.colorForm.setLayout(5, QFormLayout.ItemRole.FieldRole, self.horizontalLayout_6)


        self.verticalLayout.addLayout(self.colorForm)

        self.colorTolerancesLabel = QLabel(Form)
        self.colorTolerancesLabel.setObjectName(u"colorTolerancesLabel")
        self.colorTolerancesLabel.setTextFormat(Qt.TextFormat.MarkdownText)

        self.verticalLayout.addWidget(self.colorTolerancesLabel)

        self.colorForm_2 = QFormLayout()
        self.colorForm_2.setObjectName(u"colorForm_2")
        self.redToleranceLabel = QLabel(Form)
        self.redToleranceLabel.setObjectName(u"redToleranceLabel")

        self.colorForm_2.setWidget(0, QFormLayout.ItemRole.LabelRole, self.redToleranceLabel)

        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.redToleranceSlider = QSlider(Form)
        self.redToleranceSlider.setObjectName(u"redToleranceSlider")
        self.redToleranceSlider.setMaximum(75)
        self.redToleranceSlider.setOrientation(Qt.Orientation.Horizontal)
        self.redToleranceSlider.setTickInterval(10)

        self.horizontalLayout_7.addWidget(self.redToleranceSlider)

        self.redTolerance = QSpinBox(Form)
        self.redTolerance.setObjectName(u"redTolerance")
        self.redTolerance.setMaximum(75)

        self.horizontalLayout_7.addWidget(self.redTolerance)


        self.colorForm_2.setLayout(0, QFormLayout.ItemRole.FieldRole, self.horizontalLayout_7)

        self.yellowToleranceLabel = QLabel(Form)
        self.yellowToleranceLabel.setObjectName(u"yellowToleranceLabel")

        self.colorForm_2.setWidget(1, QFormLayout.ItemRole.LabelRole, self.yellowToleranceLabel)

        self.horizontalLayout_8 = QHBoxLayout()
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.yellowToleranceSlider = QSlider(Form)
        self.yellowToleranceSlider.setObjectName(u"yellowToleranceSlider")
        self.yellowToleranceSlider.setMaximum(75)
        self.yellowToleranceSlider.setOrientation(Qt.Orientation.Horizontal)
        self.yellowToleranceSlider.setTickInterval(10)

        self.horizontalLayout_8.addWidget(self.yellowToleranceSlider)

        self.yellowTolerance = QSpinBox(Form)
        self.yellowTolerance.setObjectName(u"yellowTolerance")
        self.yellowTolerance.setMaximum(75)

        self.horizontalLayout_8.addWidget(self.yellowTolerance)


        self.colorForm_2.setLayout(1, QFormLayout.ItemRole.FieldRole, self.horizontalLayout_8)

        self.greenToleranceLabel = QLabel(Form)
        self.greenToleranceLabel.setObjectName(u"greenToleranceLabel")

        self.colorForm_2.setWidget(2, QFormLayout.ItemRole.LabelRole, self.greenToleranceLabel)

        self.horizontalLayout_9 = QHBoxLayout()
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.greenToleranceSlider = QSlider(Form)
        self.greenToleranceSlider.setObjectName(u"greenToleranceSlider")
        self.greenToleranceSlider.setMaximum(75)
        self.greenToleranceSlider.setOrientation(Qt.Orientation.Horizontal)
        self.greenToleranceSlider.setTickInterval(10)

        self.horizontalLayout_9.addWidget(self.greenToleranceSlider)

        self.greenTolerance = QSpinBox(Form)
        self.greenTolerance.setObjectName(u"greenTolerance")
        self.greenTolerance.setMaximum(75)

        self.horizontalLayout_9.addWidget(self.greenTolerance)


        self.colorForm_2.setLayout(2, QFormLayout.ItemRole.FieldRole, self.horizontalLayout_9)

        self.cyanToleranceLabel = QLabel(Form)
        self.cyanToleranceLabel.setObjectName(u"cyanToleranceLabel")

        self.colorForm_2.setWidget(3, QFormLayout.ItemRole.LabelRole, self.cyanToleranceLabel)

        self.horizontalLayout_10 = QHBoxLayout()
        self.horizontalLayout_10.setObjectName(u"horizontalLayout_10")
        self.cyanToleranceSlider = QSlider(Form)
        self.cyanToleranceSlider.setObjectName(u"cyanToleranceSlider")
        self.cyanToleranceSlider.setMaximum(75)
        self.cyanToleranceSlider.setOrientation(Qt.Orientation.Horizontal)
        self.cyanToleranceSlider.setTickInterval(10)

        self.horizontalLayout_10.addWidget(self.cyanToleranceSlider)

        self.cyanTolerance = QSpinBox(Form)
        self.cyanTolerance.setObjectName(u"cyanTolerance")
        self.cyanTolerance.setMaximum(75)

        self.horizontalLayout_10.addWidget(self.cyanTolerance)


        self.colorForm_2.setLayout(3, QFormLayout.ItemRole.FieldRole, self.horizontalLayout_10)

        self.blueToleranceLabel = QLabel(Form)
        self.blueToleranceLabel.setObjectName(u"blueToleranceLabel")

        self.colorForm_2.setWidget(4, QFormLayout.ItemRole.LabelRole, self.blueToleranceLabel)

        self.horizontalLayout_11 = QHBoxLayout()
        self.horizontalLayout_11.setObjectName(u"horizontalLayout_11")
        self.blueToleranceSlider = QSlider(Form)
        self.blueToleranceSlider.setObjectName(u"blueToleranceSlider")
        self.blueToleranceSlider.setMaximum(75)
        self.blueToleranceSlider.setOrientation(Qt.Orientation.Horizontal)
        self.blueToleranceSlider.setTickInterval(10)

        self.horizontalLayout_11.addWidget(self.blueToleranceSlider)

        self.blueTolerance = QSpinBox(Form)
        self.blueTolerance.setObjectName(u"blueTolerance")
        self.blueTolerance.setMaximum(75)

        self.horizontalLayout_11.addWidget(self.blueTolerance)


        self.colorForm_2.setLayout(4, QFormLayout.ItemRole.FieldRole, self.horizontalLayout_11)

        self.magentaToleranceLabel = QLabel(Form)
        self.magentaToleranceLabel.setObjectName(u"magentaToleranceLabel")

        self.colorForm_2.setWidget(5, QFormLayout.ItemRole.LabelRole, self.magentaToleranceLabel)

        self.horizontalLayout_12 = QHBoxLayout()
        self.horizontalLayout_12.setObjectName(u"horizontalLayout_12")
        self.magentaToleranceSlider = QSlider(Form)
        self.magentaToleranceSlider.setObjectName(u"magentaToleranceSlider")
        self.magentaToleranceSlider.setMaximum(75)
        self.magentaToleranceSlider.setOrientation(Qt.Orientation.Horizontal)
        self.magentaToleranceSlider.setTickInterval(10)

        self.horizontalLayout_12.addWidget(self.magentaToleranceSlider)

        self.magentaTolerance = QSpinBox(Form)
        self.magentaTolerance.setObjectName(u"magentaTolerance")
        self.magentaTolerance.setMaximum(75)

        self.horizontalLayout_12.addWidget(self.magentaTolerance)


        self.colorForm_2.setLayout(5, QFormLayout.ItemRole.FieldRole, self.horizontalLayout_12)


        self.verticalLayout.addLayout(self.colorForm_2)

        self.shapeDetectionLabel = QLabel(Form)
        self.shapeDetectionLabel.setObjectName(u"shapeDetectionLabel")
        self.shapeDetectionLabel.setTextFormat(Qt.TextFormat.MarkdownText)

        self.verticalLayout.addWidget(self.shapeDetectionLabel)

        self.formLayout_2 = QFormLayout()
        self.formLayout_2.setObjectName(u"formLayout_2")
        self.classifierLabel = QLabel(Form)
        self.classifierLabel.setObjectName(u"classifierLabel")

        self.formLayout_2.setWidget(0, QFormLayout.ItemRole.LabelRole, self.classifierLabel)

        self.classifier = QComboBox(Form)
        self.classifier.setObjectName(u"classifier")

        self.formLayout_2.setWidget(0, QFormLayout.ItemRole.FieldRole, self.classifier)


        self.verticalLayout.addLayout(self.formLayout_2)

        self.trackingLabel = QLabel(Form)
        self.trackingLabel.setObjectName(u"trackingLabel")
        self.trackingLabel.setTextFormat(Qt.TextFormat.MarkdownText)

        self.verticalLayout.addWidget(self.trackingLabel)

        self.track = QPushButton(Form)
        self.track.setObjectName(u"track")

        self.verticalLayout.addWidget(self.track)

        self.reset = QPushButton(Form)
        self.reset.setObjectName(u"reset")

        self.verticalLayout.addWidget(self.reset)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.trackerMappingLabel.setText(QCoreApplication.translate("Form", u"### Tracker mapping", None))
        self.leftHandLabel.setText(QCoreApplication.translate("Form", u"Left hand", None))
        self.leftIndexLabel.setText(QCoreApplication.translate("Form", u"Index", None))
        self.leftMiddleLabel.setText(QCoreApplication.translate("Form", u"Middle", None))
        self.leftRingLabel.setText(QCoreApplication.translate("Form", u"Ring", None))
        self.leftPinkyLabel.setText(QCoreApplication.translate("Form", u"Pinky", None))
        self.leftPalmLabel.setText(QCoreApplication.translate("Form", u"Palm", None))
        self.leftThumbLabel.setText(QCoreApplication.translate("Form", u"Thumb", None))
        self.rightHandLabel.setText(QCoreApplication.translate("Form", u"Right hand", None))
        self.rightIndexLabel.setText(QCoreApplication.translate("Form", u"Index", None))
        self.rightMiddleLabel.setText(QCoreApplication.translate("Form", u"Middle", None))
        self.rightRingLabel.setText(QCoreApplication.translate("Form", u"Ring", None))
        self.rightPinkyLabel.setText(QCoreApplication.translate("Form", u"Pinky", None))
        self.rightPalmLabel.setText(QCoreApplication.translate("Form", u"Palm", None))
        self.rightThumbLabel.setText(QCoreApplication.translate("Form", u"Thumb", None))
        self.colorHuesLabel.setText(QCoreApplication.translate("Form", u"### Color hue values", None))
        self.redHueLabel.setText(QCoreApplication.translate("Form", u"Red", None))
        self.redHue.setSuffix(QCoreApplication.translate("Form", u"\u00b0", None))
        self.redHuePick.setText(QCoreApplication.translate("Form", u"Pick", None))
        self.yellowHueLabel.setText(QCoreApplication.translate("Form", u"Yellow", None))
        self.yellowHue.setSuffix(QCoreApplication.translate("Form", u"\u00b0", None))
        self.yellowHuePick.setText(QCoreApplication.translate("Form", u"Pick", None))
        self.greenHueLabel.setText(QCoreApplication.translate("Form", u"Green", None))
        self.greenHue.setSuffix(QCoreApplication.translate("Form", u"\u00b0", None))
        self.greenHuePick.setText(QCoreApplication.translate("Form", u"Pick", None))
        self.cyanHueLabel.setText(QCoreApplication.translate("Form", u"Cyan", None))
        self.cyanHue.setSuffix(QCoreApplication.translate("Form", u"\u00b0", None))
        self.cyanHuePick.setText(QCoreApplication.translate("Form", u"Pick", None))
        self.blueHueLabel.setText(QCoreApplication.translate("Form", u"Blue", None))
        self.blueHue.setSuffix(QCoreApplication.translate("Form", u"\u00b0", None))
        self.blueHuePick.setText(QCoreApplication.translate("Form", u"Pick", None))
        self.magentaHueLabel.setText(QCoreApplication.translate("Form", u"Magenta", None))
        self.magentaHue.setSuffix(QCoreApplication.translate("Form", u"\u00b0", None))
        self.magentaHuePick.setText(QCoreApplication.translate("Form", u"Pick", None))
        self.colorTolerancesLabel.setText(QCoreApplication.translate("Form", u"### Color tolerances", None))
        self.redToleranceLabel.setText(QCoreApplication.translate("Form", u"Red", None))
        self.redTolerance.setSuffix(QCoreApplication.translate("Form", u"%", None))
        self.yellowToleranceLabel.setText(QCoreApplication.translate("Form", u"Yellow", None))
        self.yellowTolerance.setSuffix(QCoreApplication.translate("Form", u"%", None))
        self.greenToleranceLabel.setText(QCoreApplication.translate("Form", u"Green", None))
        self.greenTolerance.setSuffix(QCoreApplication.translate("Form", u"%", None))
        self.cyanToleranceLabel.setText(QCoreApplication.translate("Form", u"Cyan", None))
        self.cyanTolerance.setSuffix(QCoreApplication.translate("Form", u"%", None))
        self.blueToleranceLabel.setText(QCoreApplication.translate("Form", u"Blue", None))
        self.blueTolerance.setSuffix(QCoreApplication.translate("Form", u"%", None))
        self.magentaToleranceLabel.setText(QCoreApplication.translate("Form", u"Magenta", None))
        self.magentaTolerance.setSuffix(QCoreApplication.translate("Form", u"%", None))
        self.shapeDetectionLabel.setText(QCoreApplication.translate("Form", u"### Shape detection", None))
        self.classifierLabel.setText(QCoreApplication.translate("Form", u"Classifier", None))
        self.trackingLabel.setText(QCoreApplication.translate("Form", u"### Run", None))
        self.track.setText(QCoreApplication.translate("Form", u"Start tracking", None))
        self.reset.setText(QCoreApplication.translate("Form", u"Reset tracking", None))
    # retranslateUi

