# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'calibration.ui'
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
from PySide6.QtWidgets import (QAbstractSpinBox, QApplication, QComboBox, QDoubleSpinBox,
    QFormLayout, QHBoxLayout, QLabel, QPushButton,
    QSizePolicy, QSpacerItem, QSpinBox, QVBoxLayout,
    QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(528, 703)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Form.sizePolicy().hasHeightForWidth())
        Form.setSizePolicy(sizePolicy)
        self.verticalLayout = QVBoxLayout(Form)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.timeControlLabel = QLabel(Form)
        self.timeControlLabel.setObjectName(u"timeControlLabel")
        self.timeControlLabel.setTextFormat(Qt.TextFormat.MarkdownText)

        self.verticalLayout.addWidget(self.timeControlLabel)

        self.timeControlForm = QFormLayout()
        self.timeControlForm.setObjectName(u"timeControlForm")
        self.startFrameLabel = QLabel(Form)
        self.startFrameLabel.setObjectName(u"startFrameLabel")

        self.timeControlForm.setWidget(0, QFormLayout.ItemRole.LabelRole, self.startFrameLabel)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.startFrame = QSpinBox(Form)
        self.startFrame.setObjectName(u"startFrame")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.startFrame.sizePolicy().hasHeightForWidth())
        self.startFrame.setSizePolicy(sizePolicy1)
        self.startFrame.setFrame(True)
        self.startFrame.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.PlusMinus)
        self.startFrame.setAccelerated(False)
        self.startFrame.setProperty(u"showGroupSeparator", False)
        self.startFrame.setMaximum(0)

        self.horizontalLayout.addWidget(self.startFrame)

        self.startFrameReset = QPushButton(Form)
        self.startFrameReset.setObjectName(u"startFrameReset")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.startFrameReset.sizePolicy().hasHeightForWidth())
        self.startFrameReset.setSizePolicy(sizePolicy2)
        self.startFrameReset.setFlat(False)

        self.horizontalLayout.addWidget(self.startFrameReset)


        self.timeControlForm.setLayout(0, QFormLayout.ItemRole.FieldRole, self.horizontalLayout)

        self.endFrameLabel = QLabel(Form)
        self.endFrameLabel.setObjectName(u"endFrameLabel")

        self.timeControlForm.setWidget(1, QFormLayout.ItemRole.LabelRole, self.endFrameLabel)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.endFrame = QSpinBox(Form)
        self.endFrame.setObjectName(u"endFrame")
        sizePolicy1.setHeightForWidth(self.endFrame.sizePolicy().hasHeightForWidth())
        self.endFrame.setSizePolicy(sizePolicy1)
        self.endFrame.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.PlusMinus)
        self.endFrame.setMaximum(0)

        self.horizontalLayout_2.addWidget(self.endFrame)

        self.endFrameReset = QPushButton(Form)
        self.endFrameReset.setObjectName(u"endFrameReset")
        sizePolicy2.setHeightForWidth(self.endFrameReset.sizePolicy().hasHeightForWidth())
        self.endFrameReset.setSizePolicy(sizePolicy2)
        self.endFrameReset.setFlat(False)

        self.horizontalLayout_2.addWidget(self.endFrameReset)


        self.timeControlForm.setLayout(1, QFormLayout.ItemRole.FieldRole, self.horizontalLayout_2)

        self.frameRateLabel = QLabel(Form)
        self.frameRateLabel.setObjectName(u"frameRateLabel")

        self.timeControlForm.setWidget(2, QFormLayout.ItemRole.LabelRole, self.frameRateLabel)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.frameRate = QDoubleSpinBox(Form)
        self.frameRate.setObjectName(u"frameRate")
        sizePolicy1.setHeightForWidth(self.frameRate.sizePolicy().hasHeightForWidth())
        self.frameRate.setSizePolicy(sizePolicy1)
        self.frameRate.setMaximum(999.990000000000009)

        self.horizontalLayout_3.addWidget(self.frameRate)

        self.frameRateReset = QPushButton(Form)
        self.frameRateReset.setObjectName(u"frameRateReset")
        sizePolicy2.setHeightForWidth(self.frameRateReset.sizePolicy().hasHeightForWidth())
        self.frameRateReset.setSizePolicy(sizePolicy2)
        self.frameRateReset.setFlat(False)

        self.horizontalLayout_3.addWidget(self.frameRateReset)


        self.timeControlForm.setLayout(2, QFormLayout.ItemRole.FieldRole, self.horizontalLayout_3)


        self.verticalLayout.addLayout(self.timeControlForm)

        self.perspectiveControlLabel = QLabel(Form)
        self.perspectiveControlLabel.setObjectName(u"perspectiveControlLabel")
        self.perspectiveControlLabel.setTextFormat(Qt.TextFormat.MarkdownText)

        self.verticalLayout.addWidget(self.perspectiveControlLabel)

        self.perspectiveControlForm = QFormLayout()
        self.perspectiveControlForm.setObjectName(u"perspectiveControlForm")
        self.topLeftLabel = QLabel(Form)
        self.topLeftLabel.setObjectName(u"topLeftLabel")

        self.perspectiveControlForm.setWidget(0, QFormLayout.ItemRole.LabelRole, self.topLeftLabel)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.topLeftX = QSpinBox(Form)
        self.topLeftX.setObjectName(u"topLeftX")
        sizePolicy1.setHeightForWidth(self.topLeftX.sizePolicy().hasHeightForWidth())
        self.topLeftX.setSizePolicy(sizePolicy1)

        self.horizontalLayout_4.addWidget(self.topLeftX)

        self.topLeftY = QSpinBox(Form)
        self.topLeftY.setObjectName(u"topLeftY")
        sizePolicy1.setHeightForWidth(self.topLeftY.sizePolicy().hasHeightForWidth())
        self.topLeftY.setSizePolicy(sizePolicy1)

        self.horizontalLayout_4.addWidget(self.topLeftY)

        self.topLeftReset = QPushButton(Form)
        self.topLeftReset.setObjectName(u"topLeftReset")
        sizePolicy2.setHeightForWidth(self.topLeftReset.sizePolicy().hasHeightForWidth())
        self.topLeftReset.setSizePolicy(sizePolicy2)
        self.topLeftReset.setFlat(False)

        self.horizontalLayout_4.addWidget(self.topLeftReset)


        self.perspectiveControlForm.setLayout(0, QFormLayout.ItemRole.FieldRole, self.horizontalLayout_4)

        self.topRightLabel = QLabel(Form)
        self.topRightLabel.setObjectName(u"topRightLabel")

        self.perspectiveControlForm.setWidget(1, QFormLayout.ItemRole.LabelRole, self.topRightLabel)

        self.bottomLeftLabel = QLabel(Form)
        self.bottomLeftLabel.setObjectName(u"bottomLeftLabel")

        self.perspectiveControlForm.setWidget(2, QFormLayout.ItemRole.LabelRole, self.bottomLeftLabel)

        self.bottomRightLabel = QLabel(Form)
        self.bottomRightLabel.setObjectName(u"bottomRightLabel")

        self.perspectiveControlForm.setWidget(3, QFormLayout.ItemRole.LabelRole, self.bottomRightLabel)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.topRightX = QSpinBox(Form)
        self.topRightX.setObjectName(u"topRightX")
        sizePolicy1.setHeightForWidth(self.topRightX.sizePolicy().hasHeightForWidth())
        self.topRightX.setSizePolicy(sizePolicy1)

        self.horizontalLayout_5.addWidget(self.topRightX)

        self.topRightY = QSpinBox(Form)
        self.topRightY.setObjectName(u"topRightY")
        sizePolicy1.setHeightForWidth(self.topRightY.sizePolicy().hasHeightForWidth())
        self.topRightY.setSizePolicy(sizePolicy1)

        self.horizontalLayout_5.addWidget(self.topRightY)

        self.topRightReset = QPushButton(Form)
        self.topRightReset.setObjectName(u"topRightReset")
        sizePolicy2.setHeightForWidth(self.topRightReset.sizePolicy().hasHeightForWidth())
        self.topRightReset.setSizePolicy(sizePolicy2)
        self.topRightReset.setFlat(False)

        self.horizontalLayout_5.addWidget(self.topRightReset)


        self.perspectiveControlForm.setLayout(1, QFormLayout.ItemRole.FieldRole, self.horizontalLayout_5)

        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.bottomLeftX = QSpinBox(Form)
        self.bottomLeftX.setObjectName(u"bottomLeftX")
        sizePolicy1.setHeightForWidth(self.bottomLeftX.sizePolicy().hasHeightForWidth())
        self.bottomLeftX.setSizePolicy(sizePolicy1)

        self.horizontalLayout_6.addWidget(self.bottomLeftX)

        self.bottomLeftY = QSpinBox(Form)
        self.bottomLeftY.setObjectName(u"bottomLeftY")
        sizePolicy1.setHeightForWidth(self.bottomLeftY.sizePolicy().hasHeightForWidth())
        self.bottomLeftY.setSizePolicy(sizePolicy1)

        self.horizontalLayout_6.addWidget(self.bottomLeftY)

        self.bottomLeftReset = QPushButton(Form)
        self.bottomLeftReset.setObjectName(u"bottomLeftReset")
        sizePolicy2.setHeightForWidth(self.bottomLeftReset.sizePolicy().hasHeightForWidth())
        self.bottomLeftReset.setSizePolicy(sizePolicy2)
        self.bottomLeftReset.setFlat(False)

        self.horizontalLayout_6.addWidget(self.bottomLeftReset)


        self.perspectiveControlForm.setLayout(2, QFormLayout.ItemRole.FieldRole, self.horizontalLayout_6)

        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.bottomRightX = QSpinBox(Form)
        self.bottomRightX.setObjectName(u"bottomRightX")
        sizePolicy1.setHeightForWidth(self.bottomRightX.sizePolicy().hasHeightForWidth())
        self.bottomRightX.setSizePolicy(sizePolicy1)

        self.horizontalLayout_7.addWidget(self.bottomRightX)

        self.bottomRightY = QSpinBox(Form)
        self.bottomRightY.setObjectName(u"bottomRightY")
        sizePolicy1.setHeightForWidth(self.bottomRightY.sizePolicy().hasHeightForWidth())
        self.bottomRightY.setSizePolicy(sizePolicy1)

        self.horizontalLayout_7.addWidget(self.bottomRightY)

        self.bottomRightReset = QPushButton(Form)
        self.bottomRightReset.setObjectName(u"bottomRightReset")
        sizePolicy2.setHeightForWidth(self.bottomRightReset.sizePolicy().hasHeightForWidth())
        self.bottomRightReset.setSizePolicy(sizePolicy2)
        self.bottomRightReset.setFlat(False)

        self.horizontalLayout_7.addWidget(self.bottomRightReset)


        self.perspectiveControlForm.setLayout(3, QFormLayout.ItemRole.FieldRole, self.horizontalLayout_7)


        self.verticalLayout.addLayout(self.perspectiveControlForm)

        self.cornerSelect = QPushButton(Form)
        self.cornerSelect.setObjectName(u"cornerSelect")

        self.verticalLayout.addWidget(self.cornerSelect)

        self.resizeLabel = QLabel(Form)
        self.resizeLabel.setObjectName(u"resizeLabel")
        self.resizeLabel.setTextFormat(Qt.TextFormat.MarkdownText)

        self.verticalLayout.addWidget(self.resizeLabel)

        self.resizeForm = QFormLayout()
        self.resizeForm.setObjectName(u"resizeForm")
        self.pageTemplateLabel = QLabel(Form)
        self.pageTemplateLabel.setObjectName(u"pageTemplateLabel")

        self.resizeForm.setWidget(0, QFormLayout.ItemRole.LabelRole, self.pageTemplateLabel)

        self.pageTemplate = QComboBox(Form)
        self.pageTemplate.addItem("")
        self.pageTemplate.setObjectName(u"pageTemplate")

        self.resizeForm.setWidget(0, QFormLayout.ItemRole.FieldRole, self.pageTemplate)

        self.pageWidthLabel = QLabel(Form)
        self.pageWidthLabel.setObjectName(u"pageWidthLabel")

        self.resizeForm.setWidget(1, QFormLayout.ItemRole.LabelRole, self.pageWidthLabel)

        self.pageWidth = QSpinBox(Form)
        self.pageWidth.setObjectName(u"pageWidth")
        sizePolicy1.setHeightForWidth(self.pageWidth.sizePolicy().hasHeightForWidth())
        self.pageWidth.setSizePolicy(sizePolicy1)
        self.pageWidth.setFrame(True)
        self.pageWidth.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.PlusMinus)
        self.pageWidth.setAccelerated(False)
        self.pageWidth.setProperty(u"showGroupSeparator", False)
        self.pageWidth.setMinimum(0)
        self.pageWidth.setMaximum(2000)
        self.pageWidth.setValue(0)

        self.resizeForm.setWidget(1, QFormLayout.ItemRole.FieldRole, self.pageWidth)

        self.pageHeightLabel = QLabel(Form)
        self.pageHeightLabel.setObjectName(u"pageHeightLabel")

        self.resizeForm.setWidget(2, QFormLayout.ItemRole.LabelRole, self.pageHeightLabel)

        self.pageHeight = QSpinBox(Form)
        self.pageHeight.setObjectName(u"pageHeight")
        sizePolicy1.setHeightForWidth(self.pageHeight.sizePolicy().hasHeightForWidth())
        self.pageHeight.setSizePolicy(sizePolicy1)
        self.pageHeight.setFrame(True)
        self.pageHeight.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.PlusMinus)
        self.pageHeight.setAccelerated(False)
        self.pageHeight.setProperty(u"showGroupSeparator", False)
        self.pageHeight.setMaximum(2000)

        self.resizeForm.setWidget(2, QFormLayout.ItemRole.FieldRole, self.pageHeight)

        self.resolutionLabel = QLabel(Form)
        self.resolutionLabel.setObjectName(u"resolutionLabel")

        self.resizeForm.setWidget(3, QFormLayout.ItemRole.LabelRole, self.resolutionLabel)

        self.resolution = QSpinBox(Form)
        self.resolution.setObjectName(u"resolution")
        self.resolution.setMaximum(300)

        self.resizeForm.setWidget(3, QFormLayout.ItemRole.FieldRole, self.resolution)


        self.verticalLayout.addLayout(self.resizeForm)

        self.horizontalLayout_8 = QHBoxLayout()
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.resultingSizeLabel = QLabel(Form)
        self.resultingSizeLabel.setObjectName(u"resultingSizeLabel")

        self.horizontalLayout_8.addWidget(self.resultingSizeLabel)

        self.resultingSize = QLabel(Form)
        self.resultingSize.setObjectName(u"resultingSize")
        sizePolicy3 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.resultingSize.sizePolicy().hasHeightForWidth())
        self.resultingSize.setSizePolicy(sizePolicy3)

        self.horizontalLayout_8.addWidget(self.resultingSize)


        self.verticalLayout.addLayout(self.horizontalLayout_8)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)


        self.retranslateUi(Form)

        self.startFrameReset.setDefault(False)
        self.endFrameReset.setDefault(False)
        self.frameRateReset.setDefault(False)
        self.topLeftReset.setDefault(False)
        self.topRightReset.setDefault(False)
        self.bottomLeftReset.setDefault(False)
        self.bottomRightReset.setDefault(False)


        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.timeControlLabel.setText(QCoreApplication.translate("Form", u"### Time control", None))
        self.startFrameLabel.setText(QCoreApplication.translate("Form", u"Start frame", None))
        self.startFrame.setSpecialValueText("")
        self.startFrame.setSuffix("")
        self.startFrameReset.setText(QCoreApplication.translate("Form", u"\u21ba", None))
        self.endFrameLabel.setText(QCoreApplication.translate("Form", u"End frame", None))
        self.endFrameReset.setText(QCoreApplication.translate("Form", u"\u21ba", None))
        self.frameRateLabel.setText(QCoreApplication.translate("Form", u"Framerate", None))
        self.frameRate.setSuffix(QCoreApplication.translate("Form", u" FPS", None))
        self.frameRateReset.setText(QCoreApplication.translate("Form", u"\u21ba", None))
        self.perspectiveControlLabel.setText(QCoreApplication.translate("Form", u"### Crop video", None))
        self.topLeftLabel.setText(QCoreApplication.translate("Form", u"Top left", None))
        self.topLeftX.setSuffix(QCoreApplication.translate("Form", u"px", None))
        self.topLeftX.setPrefix(QCoreApplication.translate("Form", u"x: ", None))
        self.topLeftY.setSuffix(QCoreApplication.translate("Form", u"px", None))
        self.topLeftY.setPrefix(QCoreApplication.translate("Form", u"y: ", None))
        self.topLeftReset.setText(QCoreApplication.translate("Form", u"\u21ba", None))
        self.topRightLabel.setText(QCoreApplication.translate("Form", u"Top right", None))
        self.bottomLeftLabel.setText(QCoreApplication.translate("Form", u"Bottom left", None))
        self.bottomRightLabel.setText(QCoreApplication.translate("Form", u"Bottom right", None))
        self.topRightX.setSuffix(QCoreApplication.translate("Form", u"px", None))
        self.topRightX.setPrefix(QCoreApplication.translate("Form", u"x: ", None))
        self.topRightY.setSuffix(QCoreApplication.translate("Form", u"px", None))
        self.topRightY.setPrefix(QCoreApplication.translate("Form", u"y: ", None))
        self.topRightReset.setText(QCoreApplication.translate("Form", u"\u21ba", None))
        self.bottomLeftX.setSuffix(QCoreApplication.translate("Form", u"px", None))
        self.bottomLeftX.setPrefix(QCoreApplication.translate("Form", u"x: ", None))
        self.bottomLeftY.setSuffix(QCoreApplication.translate("Form", u"px", None))
        self.bottomLeftY.setPrefix(QCoreApplication.translate("Form", u"y: ", None))
        self.bottomLeftReset.setText(QCoreApplication.translate("Form", u"\u21ba", None))
        self.bottomRightX.setSuffix(QCoreApplication.translate("Form", u"px", None))
        self.bottomRightX.setPrefix(QCoreApplication.translate("Form", u"x: ", None))
        self.bottomRightY.setSuffix(QCoreApplication.translate("Form", u"px", None))
        self.bottomRightY.setPrefix(QCoreApplication.translate("Form", u"y: ", None))
        self.bottomRightReset.setText(QCoreApplication.translate("Form", u"\u21ba", None))
        self.cornerSelect.setText(QCoreApplication.translate("Form", u"Interactive selection", None))
        self.resizeLabel.setText(QCoreApplication.translate("Form", u"### Resize", None))
        self.pageTemplateLabel.setText(QCoreApplication.translate("Form", u"Template", None))
        self.pageTemplate.setItemText(0, QCoreApplication.translate("Form", u"Custom", None))

        self.pageWidthLabel.setText(QCoreApplication.translate("Form", u"Page width", None))
        self.pageWidth.setSpecialValueText("")
        self.pageWidth.setSuffix(QCoreApplication.translate("Form", u"mm", None))
        self.pageHeightLabel.setText(QCoreApplication.translate("Form", u"Page height", None))
        self.pageHeight.setSpecialValueText("")
        self.pageHeight.setSuffix(QCoreApplication.translate("Form", u"mm", None))
        self.resolutionLabel.setText(QCoreApplication.translate("Form", u"Resolution", None))
        self.resolution.setSuffix(QCoreApplication.translate("Form", u" dpi", None))
        self.resultingSizeLabel.setText(QCoreApplication.translate("Form", u"Resulting video size: ", None))
        self.resultingSize.setText(QCoreApplication.translate("Form", u"0x0", None))
    # retranslateUi

