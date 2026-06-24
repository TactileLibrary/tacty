# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'preprocessing.ui'
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QComboBox, QFormLayout,
    QHBoxLayout, QLabel, QSizePolicy, QSlider,
    QSpacerItem, QSpinBox, QVBoxLayout, QWidget)

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
        self.denoisingLabel = QLabel(Form)
        self.denoisingLabel.setObjectName(u"denoisingLabel")
        self.denoisingLabel.setTextFormat(Qt.TextFormat.MarkdownText)

        self.verticalLayout.addWidget(self.denoisingLabel)

        self.formLayout_2 = QFormLayout()
        self.formLayout_2.setObjectName(u"formLayout_2")
        self.denoisingEnabledLabel = QLabel(Form)
        self.denoisingEnabledLabel.setObjectName(u"denoisingEnabledLabel")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.denoisingEnabledLabel.sizePolicy().hasHeightForWidth())
        self.denoisingEnabledLabel.setSizePolicy(sizePolicy1)

        self.formLayout_2.setWidget(0, QFormLayout.ItemRole.LabelRole, self.denoisingEnabledLabel)

        self.denoisingEnabled = QCheckBox(Form)
        self.denoisingEnabled.setObjectName(u"denoisingEnabled")

        self.formLayout_2.setWidget(0, QFormLayout.ItemRole.FieldRole, self.denoisingEnabled)

        self.denoisingFilterLabel = QLabel(Form)
        self.denoisingFilterLabel.setObjectName(u"denoisingFilterLabel")
        sizePolicy1.setHeightForWidth(self.denoisingFilterLabel.sizePolicy().hasHeightForWidth())
        self.denoisingFilterLabel.setSizePolicy(sizePolicy1)

        self.formLayout_2.setWidget(1, QFormLayout.ItemRole.LabelRole, self.denoisingFilterLabel)

        self.denoisingFilter = QComboBox(Form)
        self.denoisingFilter.addItem("")
        self.denoisingFilter.addItem("")
        self.denoisingFilter.addItem("")
        self.denoisingFilter.addItem("")
        self.denoisingFilter.setObjectName(u"denoisingFilter")

        self.formLayout_2.setWidget(1, QFormLayout.ItemRole.FieldRole, self.denoisingFilter)

        self.denoisingSizeLabel = QLabel(Form)
        self.denoisingSizeLabel.setObjectName(u"denoisingSizeLabel")
        sizePolicy1.setHeightForWidth(self.denoisingSizeLabel.sizePolicy().hasHeightForWidth())
        self.denoisingSizeLabel.setSizePolicy(sizePolicy1)

        self.formLayout_2.setWidget(2, QFormLayout.ItemRole.LabelRole, self.denoisingSizeLabel)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.denoisingSizeSlider = QSlider(Form)
        self.denoisingSizeSlider.setObjectName(u"denoisingSizeSlider")
        self.denoisingSizeSlider.setMinimum(3)
        self.denoisingSizeSlider.setMaximum(15)
        self.denoisingSizeSlider.setSingleStep(2)
        self.denoisingSizeSlider.setPageStep(4)
        self.denoisingSizeSlider.setOrientation(Qt.Orientation.Horizontal)

        self.horizontalLayout_2.addWidget(self.denoisingSizeSlider)

        self.denoisingSize = QSpinBox(Form)
        self.denoisingSize.setObjectName(u"denoisingSize")
        self.denoisingSize.setMinimum(1)
        self.denoisingSize.setMaximum(15)
        self.denoisingSize.setSingleStep(2)
        self.denoisingSize.setValue(3)

        self.horizontalLayout_2.addWidget(self.denoisingSize)


        self.formLayout_2.setLayout(2, QFormLayout.ItemRole.FieldRole, self.horizontalLayout_2)


        self.verticalLayout.addLayout(self.formLayout_2)

        self.backgroundLabel = QLabel(Form)
        self.backgroundLabel.setObjectName(u"backgroundLabel")
        self.backgroundLabel.setTextFormat(Qt.TextFormat.MarkdownText)

        self.verticalLayout.addWidget(self.backgroundLabel)

        self.formLayout = QFormLayout()
        self.formLayout.setObjectName(u"formLayout")
        self.formLayout.setHorizontalSpacing(6)
        self.formLayout.setVerticalSpacing(6)
        self.bgrEnabledLabel = QLabel(Form)
        self.bgrEnabledLabel.setObjectName(u"bgrEnabledLabel")
        sizePolicy1.setHeightForWidth(self.bgrEnabledLabel.sizePolicy().hasHeightForWidth())
        self.bgrEnabledLabel.setSizePolicy(sizePolicy1)

        self.formLayout.setWidget(0, QFormLayout.ItemRole.LabelRole, self.bgrEnabledLabel)

        self.bgrEnabled = QCheckBox(Form)
        self.bgrEnabled.setObjectName(u"bgrEnabled")

        self.formLayout.setWidget(0, QFormLayout.ItemRole.FieldRole, self.bgrEnabled)

        self.bgrFrameLabel = QLabel(Form)
        self.bgrFrameLabel.setObjectName(u"bgrFrameLabel")
        sizePolicy1.setHeightForWidth(self.bgrFrameLabel.sizePolicy().hasHeightForWidth())
        self.bgrFrameLabel.setSizePolicy(sizePolicy1)

        self.formLayout.setWidget(1, QFormLayout.ItemRole.LabelRole, self.bgrFrameLabel)

        self.bgrFrame = QSpinBox(Form)
        self.bgrFrame.setObjectName(u"bgrFrame")

        self.formLayout.setWidget(1, QFormLayout.ItemRole.FieldRole, self.bgrFrame)

        self.bgrToleranceLabel = QLabel(Form)
        self.bgrToleranceLabel.setObjectName(u"bgrToleranceLabel")
        sizePolicy1.setHeightForWidth(self.bgrToleranceLabel.sizePolicy().hasHeightForWidth())
        self.bgrToleranceLabel.setSizePolicy(sizePolicy1)

        self.formLayout.setWidget(2, QFormLayout.ItemRole.LabelRole, self.bgrToleranceLabel)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.bgrToleranceSlider = QSlider(Form)
        self.bgrToleranceSlider.setObjectName(u"bgrToleranceSlider")
        self.bgrToleranceSlider.setMaximum(75)
        self.bgrToleranceSlider.setOrientation(Qt.Orientation.Horizontal)

        self.horizontalLayout.addWidget(self.bgrToleranceSlider)

        self.bgrTolerance = QSpinBox(Form)
        self.bgrTolerance.setObjectName(u"bgrTolerance")
        self.bgrTolerance.setMaximum(75)

        self.horizontalLayout.addWidget(self.bgrTolerance)


        self.formLayout.setLayout(2, QFormLayout.ItemRole.FieldRole, self.horizontalLayout)


        self.verticalLayout.addLayout(self.formLayout)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.denoisingLabel.setText(QCoreApplication.translate("Form", u"### Denoising", None))
        self.denoisingEnabledLabel.setText(QCoreApplication.translate("Form", u"Enabled", None))
        self.denoisingEnabled.setText("")
#if QT_CONFIG(tooltip)
        self.denoisingFilterLabel.setToolTip(QCoreApplication.translate("Form", u"A frame with no hands or shadows", None))
#endif // QT_CONFIG(tooltip)
        self.denoisingFilterLabel.setText(QCoreApplication.translate("Form", u"Filter type", None))
        self.denoisingFilter.setItemText(0, QCoreApplication.translate("Form", u"Box", None))
        self.denoisingFilter.setItemText(1, QCoreApplication.translate("Form", u"Gaussian", None))
        self.denoisingFilter.setItemText(2, QCoreApplication.translate("Form", u"Median", None))
        self.denoisingFilter.setItemText(3, QCoreApplication.translate("Form", u"Bilateral", None))

#if QT_CONFIG(tooltip)
        self.denoisingSizeLabel.setToolTip(QCoreApplication.translate("Form", u"A frame with no hands or shadows", None))
#endif // QT_CONFIG(tooltip)
        self.denoisingSizeLabel.setText(QCoreApplication.translate("Form", u"Size", None))
        self.denoisingSize.setSuffix(QCoreApplication.translate("Form", u"px", None))
        self.backgroundLabel.setText(QCoreApplication.translate("Form", u"### Background removal", None))
        self.bgrEnabledLabel.setText(QCoreApplication.translate("Form", u"Enabled", None))
        self.bgrEnabled.setText("")
#if QT_CONFIG(tooltip)
        self.bgrFrameLabel.setToolTip(QCoreApplication.translate("Form", u"A frame with no hands or shadows", None))
#endif // QT_CONFIG(tooltip)
        self.bgrFrameLabel.setText(QCoreApplication.translate("Form", u"Clean frame", None))
#if QT_CONFIG(tooltip)
        self.bgrToleranceLabel.setToolTip(QCoreApplication.translate("Form", u"How much the background is allowed to differ from the clean frame", None))
#endif // QT_CONFIG(tooltip)
        self.bgrToleranceLabel.setText(QCoreApplication.translate("Form", u"Tolerance", None))
        self.bgrTolerance.setSuffix(QCoreApplication.translate("Form", u"%", None))
    # retranslateUi

