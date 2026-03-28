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
from PySide6.QtWidgets import (QAbstractSpinBox, QApplication, QDoubleSpinBox, QFormLayout,
    QLabel, QSizePolicy, QSpinBox, QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(300, 500)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Form.sizePolicy().hasHeightForWidth())
        Form.setSizePolicy(sizePolicy)
        self.formLayout = QFormLayout(Form)
        self.formLayout.setObjectName(u"formLayout")
        self.timeControlLabel = QLabel(Form)
        self.timeControlLabel.setObjectName(u"timeControlLabel")

        self.formLayout.setWidget(0, QFormLayout.ItemRole.LabelRole, self.timeControlLabel)

        self.startFrameLabel = QLabel(Form)
        self.startFrameLabel.setObjectName(u"startFrameLabel")

        self.formLayout.setWidget(1, QFormLayout.ItemRole.LabelRole, self.startFrameLabel)

        self.endFrameLabel = QLabel(Form)
        self.endFrameLabel.setObjectName(u"endFrameLabel")

        self.formLayout.setWidget(2, QFormLayout.ItemRole.LabelRole, self.endFrameLabel)

        self.startFrame = QSpinBox(Form)
        self.startFrame.setObjectName(u"startFrame")
        self.startFrame.setFrame(True)
        self.startFrame.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.PlusMinus)
        self.startFrame.setAccelerated(False)
        self.startFrame.setProperty(u"showGroupSeparator", False)
        self.startFrame.setMaximum(0)

        self.formLayout.setWidget(1, QFormLayout.ItemRole.FieldRole, self.startFrame)

        self.endFrame = QSpinBox(Form)
        self.endFrame.setObjectName(u"endFrame")
        self.endFrame.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.PlusMinus)
        self.endFrame.setMaximum(0)

        self.formLayout.setWidget(2, QFormLayout.ItemRole.FieldRole, self.endFrame)

        self.frameRateLabel = QLabel(Form)
        self.frameRateLabel.setObjectName(u"frameRateLabel")

        self.formLayout.setWidget(3, QFormLayout.ItemRole.LabelRole, self.frameRateLabel)

        self.frameRate = QDoubleSpinBox(Form)
        self.frameRate.setObjectName(u"frameRate")
        self.frameRate.setMaximum(999.990000000000009)

        self.formLayout.setWidget(3, QFormLayout.ItemRole.FieldRole, self.frameRate)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.timeControlLabel.setText(QCoreApplication.translate("Form", u"Time control", None))
        self.startFrameLabel.setText(QCoreApplication.translate("Form", u"Start frame", None))
        self.endFrameLabel.setText(QCoreApplication.translate("Form", u"End frame", None))
        self.startFrame.setSpecialValueText("")
        self.startFrame.setSuffix("")
        self.frameRateLabel.setText(QCoreApplication.translate("Form", u"Framerate", None))
        self.frameRate.setSuffix(QCoreApplication.translate("Form", u" FPS", None))
    # retranslateUi

