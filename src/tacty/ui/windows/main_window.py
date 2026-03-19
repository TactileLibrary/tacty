from typing import override

from PySide6.QtCore import (
    QByteArray,
    QCoreApplication,
    QFile,
    QIODevice,
    QIODeviceBase,
    QJsonDocument,
    QJsonValue,
    QSettings,
    QTextStream,
    Signal,
    qInfo,
)
from PySide6.QtGui import QAction, QActionGroup, QCloseEvent, QTextDocument
from PySide6.QtWidgets import (
    QErrorMessage,
    QFileDialog,
    QMainWindow,
    QMenu,
    QMessageBox,
)

from tacty.ui.views import WelcomeView


class MainWindow(QMainWindow):
    # Signals
    themeChanged: Signal = Signal()

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
        welcomeView = WelcomeView()
        _ = welcomeView.openProject.connect(self.openProject)
        _ = welcomeView.newProject.connect(self.newProject)
        self.setCentralWidget(welcomeView)

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
        _ = fileMenu.addAction("&New", "Ctrl+N", self.newProject)
        _ = fileMenu.addAction("&Open", "Ctrl+O", self.openProject)
        _ = fileMenu.addAction("&Quit", "Ctrl+Q", self.close)
        _ = self.menuBar().addMenu(fileMenu)

        # View menu
        themes = ["light", "dark"]
        colors = ["blue", "cyan", "green", "pink", "purple", "red"]
        settings = QSettings()
        settings.beginGroup("appearance")
        currentTheme = settings.value("theme", type=str) or "dark"
        currentColor = settings.value("color", type=str) or "blue"
        settings.endGroup()
        viewMenu = QMenu("&View")
        themeMenu = QMenu("&Theme")
        themeGroup = QActionGroup(self)
        for theme in themes:
            themeAction = QAction(theme.capitalize(), themeMenu, checkable=True)
            themeAction.setData(theme)
            _ = themeGroup.addAction(themeAction)
            _ = themeMenu.addAction(themeAction)
            if currentTheme == theme:
                themeAction.setChecked(True)
        themeGroup.setExclusive(True)
        _ = themeGroup.triggered.connect(self.changeTheme)
        _ = viewMenu.addMenu(themeMenu)
        colorMenu = QMenu("&Color")
        colorGroup = QActionGroup(self)
        for color in colors:
            colorAction = QAction(color.capitalize(), colorMenu, checkable=True)
            colorAction.setData(color)
            _ = colorGroup.addAction(colorAction)
            _ = colorMenu.addAction(colorAction)
            if currentColor == color:
                colorAction.setChecked(True)
        colorGroup.setExclusive(True)
        _ = colorGroup.triggered.connect(self.changeColor)
        _ = viewMenu.addMenu(colorMenu)
        _ = self.menuBar().addMenu(viewMenu)

        # About menu
        aboutMenu = QMenu("&About")
        _ = aboutMenu.addAction("About &Tacty", self.showAbout)
        _ = aboutMenu.addAction("About &QT", self.showAboutQt)
        _ = self.menuBar().addMenu(aboutMenu)

    def openProject(self) -> None:
        name, _ = QFileDialog.getOpenFileName(
            self, "Open project", "", "Tacty Project (*.tproj)"
        )
        qInfo(f"Project opened: {name}")

    def newProject(self) -> None:
        name, _ = QFileDialog.getSaveFileName(
            self, "New project", "", "Tacty Project (*.tproj)"
        )
        if name:
            json = QJsonDocument({"projectVersion": QJsonValue(1)})
            file = QFile(name)
            opened = file.open(
                QIODeviceBase.OpenModeFlag.NewOnly
                | QIODeviceBase.OpenModeFlag.WriteOnly
            )
            if not opened:
                err = QErrorMessage(self)
                err.showMessage("Open failed. Perhaps the file already exists?")
                return
            written = file.write(json.toJson())
            if written == -1:
                err = QErrorMessage(self)
                err.showMessage("Write failed.")
                return
            file.close()
            qInfo(f"New project created: {name}")

    def changeTheme(self, action: QAction):
        settings = QSettings()
        settings.beginGroup("appearance")
        settings.setValue("theme", action.data())
        settings.endGroup()
        self.themeChanged.emit()

    def changeColor(self, action: QAction):
        settings = QSettings()
        settings.beginGroup("appearance")
        settings.setValue("color", action.data())
        settings.endGroup()
        self.themeChanged.emit()

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
            "theme": "Stylesheets provided by [BreezeStyleSheets](https://github.com/Alexhuszagh/BreezeStyleSheets/).",
            "version": f"Current version: v{QCoreApplication.applicationVersion()}",
        }
        aboutText = template.format(**templateValues)
        doc = QTextDocument()
        doc.setMarkdown(aboutText)
        html_doc = doc.toHtml()
        QMessageBox.about(self, "About", html_doc)

    def showAboutQt(self) -> None:
        QMessageBox.aboutQt(self)
