# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'export.ui'
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
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QLabel, QPushButton,
    QSizePolicy, QSpacerItem, QVBoxLayout, QWidget)

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
        self.positionDataLabel = QLabel(Form)
        self.positionDataLabel.setObjectName(u"positionDataLabel")
        self.positionDataLabel.setTextFormat(Qt.TextFormat.MarkdownText)

        self.verticalLayout.addWidget(self.positionDataLabel)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.positionCSV = QPushButton(Form)
        self.positionCSV.setObjectName(u"positionCSV")

        self.horizontalLayout.addWidget(self.positionCSV)

        self.positionXLSX = QPushButton(Form)
        self.positionXLSX.setObjectName(u"positionXLSX")

        self.horizontalLayout.addWidget(self.positionXLSX)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.positionDataLabel.setText(QCoreApplication.translate("Form", u"### Position data", None))
        self.positionCSV.setText(QCoreApplication.translate("Form", u"Export .csv", None))
        self.positionXLSX.setText(QCoreApplication.translate("Form", u"Export .xlsx", None))
    # retranslateUi

