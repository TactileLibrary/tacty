# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'postprocessing.ui'
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QHBoxLayout, QHeaderView,
    QLabel, QPushButton, QSizePolicy, QSpacerItem,
    QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget)

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
        self.outlierLabel = QLabel(Form)
        self.outlierLabel.setObjectName(u"outlierLabel")
        self.outlierLabel.setTextFormat(Qt.TextFormat.MarkdownText)

        self.verticalLayout.addWidget(self.outlierLabel)

        self.outlierAnatomy = QCheckBox(Form)
        self.outlierAnatomy.setObjectName(u"outlierAnatomy")

        self.verticalLayout.addWidget(self.outlierAnatomy)

        self.outlierSpeed = QCheckBox(Form)
        self.outlierSpeed.setObjectName(u"outlierSpeed")

        self.verticalLayout.addWidget(self.outlierSpeed)

        self.missingLabel = QLabel(Form)
        self.missingLabel.setObjectName(u"missingLabel")
        self.missingLabel.setTextFormat(Qt.TextFormat.MarkdownText)

        self.verticalLayout.addWidget(self.missingLabel)

        self.interpolation = QCheckBox(Form)
        self.interpolation.setObjectName(u"interpolation")

        self.verticalLayout.addWidget(self.interpolation)

        self.AOILabel = QLabel(Form)
        self.AOILabel.setObjectName(u"AOILabel")
        self.AOILabel.setTextFormat(Qt.TextFormat.MarkdownText)

        self.verticalLayout.addWidget(self.AOILabel)

        self.AOITable = QTableWidget(Form)
        self.AOITable.setObjectName(u"AOITable")

        self.verticalLayout.addWidget(self.AOITable)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.AOIAddRect = QPushButton(Form)
        self.AOIAddRect.setObjectName(u"AOIAddRect")

        self.horizontalLayout.addWidget(self.AOIAddRect)

        self.AOIAddPoly = QPushButton(Form)
        self.AOIAddPoly.setObjectName(u"AOIAddPoly")

        self.horizontalLayout.addWidget(self.AOIAddPoly)

        self.AOIDelete = QPushButton(Form)
        self.AOIDelete.setObjectName(u"AOIDelete")

        self.horizontalLayout.addWidget(self.AOIDelete)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.outlierLabel.setText(QCoreApplication.translate("Form", u"### Outlier removal", None))
#if QT_CONFIG(tooltip)
        self.outlierAnatomy.setToolTip(QCoreApplication.translate("Form", u"Removes finger markers that are too close or too far from the palm marker", None))
#endif // QT_CONFIG(tooltip)
        self.outlierAnatomy.setText(QCoreApplication.translate("Form", u"Detect by kinematic constaint", None))
#if QT_CONFIG(tooltip)
        self.outlierSpeed.setToolTip(QCoreApplication.translate("Form", u"Removes markers that are moving too fast", None))
#endif // QT_CONFIG(tooltip)
        self.outlierSpeed.setText(QCoreApplication.translate("Form", u"Detect by speed", None))
        self.missingLabel.setText(QCoreApplication.translate("Form", u"### Fill missing data", None))
        self.interpolation.setText(QCoreApplication.translate("Form", u"Fill gaps using interpolated data", None))
        self.AOILabel.setText(QCoreApplication.translate("Form", u"### Areas of interest", None))
        self.AOIAddRect.setText(QCoreApplication.translate("Form", u"Add rectangle", None))
        self.AOIAddPoly.setText(QCoreApplication.translate("Form", u"Add polygon", None))
        self.AOIDelete.setText(QCoreApplication.translate("Form", u"Delete selected", None))
    # retranslateUi

