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
from PySide6.QtWidgets import (QApplication, QFormLayout, QHBoxLayout, QLabel,
    QPushButton, QSizePolicy, QSlider, QSpacerItem,
    QSpinBox, QVBoxLayout, QWidget)

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

        self.colorHuesLabel_2 = QLabel(Form)
        self.colorHuesLabel_2.setObjectName(u"colorHuesLabel_2")
        self.colorHuesLabel_2.setTextFormat(Qt.TextFormat.MarkdownText)

        self.verticalLayout.addWidget(self.colorHuesLabel_2)

        self.colorForm_2 = QFormLayout()
        self.colorForm_2.setObjectName(u"colorForm_2")
        self.redToleranceLabel = QLabel(Form)
        self.redToleranceLabel.setObjectName(u"redToleranceLabel")

        self.colorForm_2.setWidget(0, QFormLayout.ItemRole.LabelRole, self.redToleranceLabel)

        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.redToleranceSlider = QSlider(Form)
        self.redToleranceSlider.setObjectName(u"redToleranceSlider")
        self.redToleranceSlider.setMaximum(100)
        self.redToleranceSlider.setOrientation(Qt.Orientation.Horizontal)
        self.redToleranceSlider.setTickInterval(10)

        self.horizontalLayout_7.addWidget(self.redToleranceSlider)

        self.redTolerance = QSpinBox(Form)
        self.redTolerance.setObjectName(u"redTolerance")
        self.redTolerance.setMaximum(100)

        self.horizontalLayout_7.addWidget(self.redTolerance)


        self.colorForm_2.setLayout(0, QFormLayout.ItemRole.FieldRole, self.horizontalLayout_7)

        self.yellowToleranceLabel = QLabel(Form)
        self.yellowToleranceLabel.setObjectName(u"yellowToleranceLabel")

        self.colorForm_2.setWidget(1, QFormLayout.ItemRole.LabelRole, self.yellowToleranceLabel)

        self.horizontalLayout_8 = QHBoxLayout()
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.yellowToleranceSlider = QSlider(Form)
        self.yellowToleranceSlider.setObjectName(u"yellowToleranceSlider")
        self.yellowToleranceSlider.setMaximum(100)
        self.yellowToleranceSlider.setOrientation(Qt.Orientation.Horizontal)
        self.yellowToleranceSlider.setTickInterval(10)

        self.horizontalLayout_8.addWidget(self.yellowToleranceSlider)

        self.yellowTolerance = QSpinBox(Form)
        self.yellowTolerance.setObjectName(u"yellowTolerance")
        self.yellowTolerance.setMaximum(100)

        self.horizontalLayout_8.addWidget(self.yellowTolerance)


        self.colorForm_2.setLayout(1, QFormLayout.ItemRole.FieldRole, self.horizontalLayout_8)

        self.greenToleranceLabel = QLabel(Form)
        self.greenToleranceLabel.setObjectName(u"greenToleranceLabel")

        self.colorForm_2.setWidget(2, QFormLayout.ItemRole.LabelRole, self.greenToleranceLabel)

        self.horizontalLayout_9 = QHBoxLayout()
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.greenToleranceSlider = QSlider(Form)
        self.greenToleranceSlider.setObjectName(u"greenToleranceSlider")
        self.greenToleranceSlider.setMaximum(100)
        self.greenToleranceSlider.setOrientation(Qt.Orientation.Horizontal)
        self.greenToleranceSlider.setTickInterval(10)

        self.horizontalLayout_9.addWidget(self.greenToleranceSlider)

        self.greenTolerance = QSpinBox(Form)
        self.greenTolerance.setObjectName(u"greenTolerance")
        self.greenTolerance.setMaximum(100)

        self.horizontalLayout_9.addWidget(self.greenTolerance)


        self.colorForm_2.setLayout(2, QFormLayout.ItemRole.FieldRole, self.horizontalLayout_9)

        self.cyanToleranceLabel = QLabel(Form)
        self.cyanToleranceLabel.setObjectName(u"cyanToleranceLabel")

        self.colorForm_2.setWidget(3, QFormLayout.ItemRole.LabelRole, self.cyanToleranceLabel)

        self.horizontalLayout_10 = QHBoxLayout()
        self.horizontalLayout_10.setObjectName(u"horizontalLayout_10")
        self.cyanToleranceSlider = QSlider(Form)
        self.cyanToleranceSlider.setObjectName(u"cyanToleranceSlider")
        self.cyanToleranceSlider.setMaximum(100)
        self.cyanToleranceSlider.setOrientation(Qt.Orientation.Horizontal)
        self.cyanToleranceSlider.setTickInterval(10)

        self.horizontalLayout_10.addWidget(self.cyanToleranceSlider)

        self.cyanTolerance = QSpinBox(Form)
        self.cyanTolerance.setObjectName(u"cyanTolerance")
        self.cyanTolerance.setMaximum(100)

        self.horizontalLayout_10.addWidget(self.cyanTolerance)


        self.colorForm_2.setLayout(3, QFormLayout.ItemRole.FieldRole, self.horizontalLayout_10)

        self.blueToleranceLabel = QLabel(Form)
        self.blueToleranceLabel.setObjectName(u"blueToleranceLabel")

        self.colorForm_2.setWidget(4, QFormLayout.ItemRole.LabelRole, self.blueToleranceLabel)

        self.horizontalLayout_11 = QHBoxLayout()
        self.horizontalLayout_11.setObjectName(u"horizontalLayout_11")
        self.blueToleranceSlider = QSlider(Form)
        self.blueToleranceSlider.setObjectName(u"blueToleranceSlider")
        self.blueToleranceSlider.setMaximum(100)
        self.blueToleranceSlider.setOrientation(Qt.Orientation.Horizontal)
        self.blueToleranceSlider.setTickInterval(10)

        self.horizontalLayout_11.addWidget(self.blueToleranceSlider)

        self.blueTolerance = QSpinBox(Form)
        self.blueTolerance.setObjectName(u"blueTolerance")
        self.blueTolerance.setMaximum(100)

        self.horizontalLayout_11.addWidget(self.blueTolerance)


        self.colorForm_2.setLayout(4, QFormLayout.ItemRole.FieldRole, self.horizontalLayout_11)

        self.magentaToleranceLabel = QLabel(Form)
        self.magentaToleranceLabel.setObjectName(u"magentaToleranceLabel")

        self.colorForm_2.setWidget(5, QFormLayout.ItemRole.LabelRole, self.magentaToleranceLabel)

        self.horizontalLayout_12 = QHBoxLayout()
        self.horizontalLayout_12.setObjectName(u"horizontalLayout_12")
        self.magentaToleranceSlider = QSlider(Form)
        self.magentaToleranceSlider.setObjectName(u"magentaToleranceSlider")
        self.magentaToleranceSlider.setMaximum(100)
        self.magentaToleranceSlider.setOrientation(Qt.Orientation.Horizontal)
        self.magentaToleranceSlider.setTickInterval(10)

        self.horizontalLayout_12.addWidget(self.magentaToleranceSlider)

        self.magentaTolerance = QSpinBox(Form)
        self.magentaTolerance.setObjectName(u"magentaTolerance")
        self.magentaTolerance.setMaximum(100)

        self.horizontalLayout_12.addWidget(self.magentaTolerance)


        self.colorForm_2.setLayout(5, QFormLayout.ItemRole.FieldRole, self.horizontalLayout_12)


        self.verticalLayout.addLayout(self.colorForm_2)

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
        self.colorHuesLabel_2.setText(QCoreApplication.translate("Form", u"### Color tolerances", None))
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
        self.trackingLabel.setText(QCoreApplication.translate("Form", u"### Run", None))
        self.track.setText(QCoreApplication.translate("Form", u"Start tracking", None))
        self.reset.setText(QCoreApplication.translate("Form", u"Reset tracking", None))
    # retranslateUi

