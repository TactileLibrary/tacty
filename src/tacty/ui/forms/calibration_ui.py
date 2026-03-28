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
    QHBoxLayout, QLabel, QPushButton, QSizePolicy,
    QSpinBox, QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(528, 500)
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

        self.formLayout.setWidget(2, QFormLayout.ItemRole.LabelRole, self.startFrameLabel)

        self.endFrameLabel = QLabel(Form)
        self.endFrameLabel.setObjectName(u"endFrameLabel")

        self.formLayout.setWidget(3, QFormLayout.ItemRole.LabelRole, self.endFrameLabel)

        self.frameRateLabel = QLabel(Form)
        self.frameRateLabel.setObjectName(u"frameRateLabel")

        self.formLayout.setWidget(4, QFormLayout.ItemRole.LabelRole, self.frameRateLabel)

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


        self.formLayout.setLayout(2, QFormLayout.ItemRole.FieldRole, self.horizontalLayout)

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


        self.formLayout.setLayout(3, QFormLayout.ItemRole.FieldRole, self.horizontalLayout_2)

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


        self.formLayout.setLayout(4, QFormLayout.ItemRole.FieldRole, self.horizontalLayout_3)


        self.retranslateUi(Form)

        self.startFrameReset.setDefault(False)
        self.endFrameReset.setDefault(False)
        self.frameRateReset.setDefault(False)


        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.timeControlLabel.setText(QCoreApplication.translate("Form", u"Time control", None))
        self.startFrameLabel.setText(QCoreApplication.translate("Form", u"Start frame", None))
        self.endFrameLabel.setText(QCoreApplication.translate("Form", u"End frame", None))
        self.frameRateLabel.setText(QCoreApplication.translate("Form", u"Framerate", None))
        self.startFrame.setSpecialValueText("")
        self.startFrame.setSuffix("")
        self.startFrameReset.setText(QCoreApplication.translate("Form", u"\u21ba", None))
        self.endFrameReset.setText(QCoreApplication.translate("Form", u"\u21ba", None))
        self.frameRate.setSuffix(QCoreApplication.translate("Form", u" FPS", None))
        self.frameRateReset.setText(QCoreApplication.translate("Form", u"\u21ba", None))
    # retranslateUi

