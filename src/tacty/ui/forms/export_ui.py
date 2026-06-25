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
        self.flatCSV = QPushButton(Form)
        self.flatCSV.setObjectName(u"flatCSV")

        self.horizontalLayout.addWidget(self.flatCSV)

        self.flatXLSX = QPushButton(Form)
        self.flatXLSX.setObjectName(u"flatXLSX")

        self.horizontalLayout.addWidget(self.flatXLSX)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.heatmapsLabel = QLabel(Form)
        self.heatmapsLabel.setObjectName(u"heatmapsLabel")
        self.heatmapsLabel.setTextFormat(Qt.TextFormat.MarkdownText)

        self.verticalLayout.addWidget(self.heatmapsLabel)

        self.heatmaps = QPushButton(Form)
        self.heatmaps.setObjectName(u"heatmaps")

        self.verticalLayout.addWidget(self.heatmaps)

        self.connectorsLabel = QLabel(Form)
        self.connectorsLabel.setObjectName(u"connectorsLabel")
        self.connectorsLabel.setTextFormat(Qt.TextFormat.MarkdownText)

        self.verticalLayout.addWidget(self.connectorsLabel)

        self.gazePlotterLabel = QLabel(Form)
        self.gazePlotterLabel.setObjectName(u"gazePlotterLabel")
        self.gazePlotterLabel.setTextFormat(Qt.TextFormat.MarkdownText)
        self.gazePlotterLabel.setScaledContents(False)
        self.gazePlotterLabel.setWordWrap(True)
        self.gazePlotterLabel.setOpenExternalLinks(True)

        self.verticalLayout.addWidget(self.gazePlotterLabel)

        self.gazePlotter = QPushButton(Form)
        self.gazePlotter.setObjectName(u"gazePlotter")

        self.verticalLayout.addWidget(self.gazePlotter)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.positionDataLabel.setText(QCoreApplication.translate("Form", u"### Flat data", None))
        self.flatCSV.setText(QCoreApplication.translate("Form", u"Export .csv", None))
        self.flatXLSX.setText(QCoreApplication.translate("Form", u"Export .xlsx", None))
        self.heatmapsLabel.setText(QCoreApplication.translate("Form", u"### Heatmaps", None))
        self.heatmaps.setText(QCoreApplication.translate("Form", u"Export to folder", None))
        self.connectorsLabel.setText(QCoreApplication.translate("Form", u"### Connectors", None))
        self.gazePlotterLabel.setText(QCoreApplication.translate("Form", u"#### GazePlotter\n"
" GazePlotter is a free web application for eye-tracking data analysis and visualization. Built with a commitment to open science, GazePlotter transforms complex gaze data into intuitive, interactive visualizations without requiring registration, subscriptions, or server uploads.\n"
"\n"
"More information on [the official website](https://gazeplotter.com/).", None))
        self.gazePlotter.setText(QCoreApplication.translate("Form", u"Export to GazePlotter", None))
    # retranslateUi

