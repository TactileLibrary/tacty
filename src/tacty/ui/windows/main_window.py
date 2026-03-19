from typing import override

from PySide6.QtCore import (
    QByteArray,
    QCoreApplication,
    QFile,
    QIODevice,
    QSettings,
    Qt,
    QTextStream,
)
from PySide6.QtGui import QActionGroup, QCloseEvent, QTextDocument
from PySide6.QtWidgets import QApplication, QFileDialog, QMainWindow, QMenu, QMessageBox

from tacty.ui.views import WelcomeView


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        settings = QSettings()

        # Set window details.
        self.setWindowTitle
        self.setMinimumSize(800, 450)

        # Restore previous window state.
        settings.beginGroup("window")
        geometry = settings.value("geometry", type=QByteArray)
        if isinstance(geometry, QByteArray):
            _ = self.restoreGeometry(geometry)
        maximized = settings.value("maximized", type=bool)
        if isinstance(maximized, bool) and maximized:
            self.showMaximized()
        settings.endGroup()

        # Set the menu bar.
        self.initMenuBar()

        # Show the welcome screen.
        self.setCentralWidget(WelcomeView())

    @override
    def closeEvent(self, event: QCloseEvent):
        # Save window state.
        settings = QSettings()
        settings.beginGroup("window")
        settings.setValue("geometry", self.saveGeometry())
        settings.setValue("maximized", self.isMaximized())
        settings.endGroup()

        super().closeEvent(event)

    def initMenuBar(self) -> None:
        # File menu
        fileMenu = QMenu("&File")
        _ = fileMenu.addAction("&New", "Ctrl+N")
        _ = fileMenu.addAction("&Open", "Ctrl+O", self.openProject)
        _ = fileMenu.addAction("&Quit", "Ctrl+Q", self.close)
        _ = self.menuBar().addMenu(fileMenu)

        # View menu
        viewMenu = QMenu("&View")
        themeMenu = QMenu("&Theme")
        themeGroup = QActionGroup(self)
        darkAction = themeMenu.addAction("&Dark", self.disableLightMode)
        darkAction.setCheckable(True)
        _ = themeGroup.addAction(darkAction)
        lightAction = themeMenu.addAction("&Light", self.enableLightMode)
        lightAction.setCheckable(True)
        _ = themeGroup.addAction(lightAction)
        themeGroup.setExclusive(True)
        _ = viewMenu.addMenu(themeMenu)
        _ = self.menuBar().addMenu(viewMenu)

        if QSettings().value("lightMode", type=bool):
            lightAction.setChecked(True)
        else:
            darkAction.setChecked(True)

        # About menu
        aboutMenu = QMenu("&About")
        _ = aboutMenu.addAction("About &Tacty", self.showAbout)
        _ = aboutMenu.addAction("About &QT", self.showAboutQt)
        _ = self.menuBar().addMenu(aboutMenu)

    def openProject(self) -> None:
        name, _ = QFileDialog.getOpenFileName(
            self, "Open project", "", "Tacty Project (*.tproj)"
        )
        print(name)

    def enableLightMode(self) -> None:
        QApplication.styleHints().setColorScheme(Qt.ColorScheme.Light)
        settings = QSettings()
        settings.setValue("lightMode", True)

    def disableLightMode(self) -> None:
        QApplication.styleHints().setColorScheme(Qt.ColorScheme.Dark)
        settings = QSettings()
        settings.setValue("lightMode", False)

    def showAbout(self) -> None:
        file = QFile(":templates/about.md")
        _ = file.open(
            QIODevice.OpenModeFlag.ReadOnly | QIODevice.OpenModeFlag.Text
        )  # TODO: proper error handling
        template = QTextStream(file).readAll()
        file.close()
        templateValues = {
            "title": "About Tacty",
            "description": "Tacty is an open source integrated tactile interaction analysis toolkit.",
            "developers": "Development is lead by [Iulian Rotaru](https://www.linkedin.com/in/iulian-rotaru-6147b5284/) as part of the [TactileLibrary](https://tactilelibrary.net) research center of the [West University of Timișoara](https://www.uvt.ro/en/).",
            "icons": "Icons provided by [heroicons](https://heroicons.com/).",
            "version": f"Current version: v{QCoreApplication.applicationVersion()}",
        }
        aboutText = template.format(**templateValues)
        doc = QTextDocument()
        doc.setMarkdown(aboutText)
        html_doc = doc.toHtml()
        QMessageBox.about(self, "About", html_doc)

    def showAboutQt(self) -> None:
        QMessageBox.aboutQt(self)
