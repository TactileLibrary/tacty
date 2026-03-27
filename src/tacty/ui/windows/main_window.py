from typing import override

import cv2
from PySide6.QtCore import (
    QByteArray,
    QCoreApplication,
    QFile,
    QFileInfo,
    QIODevice,
    QIODeviceBase,
    QSettings,
    QTextStream,
    Signal,
    qInfo,
)
from PySide6.QtGui import QAction, QActionGroup, QCloseEvent, QTextDocument
from PySide6.QtWidgets import (
    QDialog,
    QErrorMessage,
    QFileDialog,
    QMainWindow,
    QMenu,
    QMessageBox,
)

from tacty.ui.models.project import CalibrationOptions, Duration, Project
from tacty.ui.utils.hash import getHashFromPath
from tacty.ui.views import WelcomeView
from tacty.ui.views.project_view import ProjectView
from tacty.ui.windows.new_project_modal import NewProjectModal


class MainWindow(QMainWindow):
    # Signals
    themeChanged: Signal = Signal()

    # Dynamic menus
    saveAction: QAction
    saveAsAction: QAction
    closeAction: QAction
    colorMenu: QMenu

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
        self.showWelcome()

    @override
    def closeEvent(self, event: QCloseEvent):
        # Save window state.
        settings = QSettings()
        settings.beginGroup("window")
        settings.setValue("geometry", self.saveGeometry())
        settings.setValue("maximized", self.isMaximized())
        settings.endGroup()

        super().closeEvent(event)

    def showWelcome(self):
        welcomeView = WelcomeView()
        _ = welcomeView.openProject.connect(self.openProject)
        _ = welcomeView.newProject.connect(self.newProject)
        self.setCentralWidget(welcomeView)

        self.saveAction.setEnabled(False)
        self.saveAsAction.setEnabled(False)
        self.closeAction.setEnabled(False)

    def showProject(self, project: Project):
        projectView = ProjectView(project)

        self.setCentralWidget(projectView)

        self.saveAction.setEnabled(True)
        self.saveAsAction.setEnabled(True)
        self.closeAction.setEnabled(True)

    def initMenuBar(self) -> None:
        # File menu
        fileMenu = QMenu("&File")
        _ = fileMenu.addAction("&New", "Ctrl+N", self.newProject)
        _ = fileMenu.addAction("&Open", "Ctrl+O", self.openProject)
        _ = fileMenu.addSeparator()
        self.saveAction = fileMenu.addAction("&Save project", "Ctrl+S")
        self.saveAsAction = fileMenu.addAction("Save project &as...", "Ctrl+Alt+S")
        self.closeAction = fileMenu.addAction("&Close project", self.closeProject)
        _ = fileMenu.addSeparator()
        _ = fileMenu.addAction("&Quit", "Ctrl+Q", self.close)
        _ = self.menuBar().addMenu(fileMenu)

        # View menu
        themes = [
            ("native", "Native"),
            ("light", "Breeze Light"),
            ("dark", "Breeze Dark"),
        ]
        colors = ["blue", "cyan", "green", "pink", "purple", "red"]
        settings = QSettings()
        settings.beginGroup("appearance")
        currentTheme = settings.value("theme", type=str) or "native"
        currentColor = settings.value("color", type=str) or "blue"
        settings.endGroup()
        viewMenu = QMenu("&View")
        themeMenu = QMenu("&Theme")
        themeGroup = QActionGroup(self)
        for theme in themes:
            themeAction = QAction(theme[1], themeMenu, checkable=True)
            themeAction.setData(theme[0])
            _ = themeGroup.addAction(themeAction)
            _ = themeMenu.addAction(themeAction)
            if currentTheme == theme[0]:
                themeAction.setChecked(True)
        themeGroup.setExclusive(True)
        _ = themeGroup.triggered.connect(self.changeTheme)
        _ = viewMenu.addMenu(themeMenu)
        self.colorMenu = QMenu("&Color")
        if currentTheme == "native":
            self.colorMenu.setEnabled(False)
        colorGroup = QActionGroup(self)
        for color in colors:
            colorAction = QAction(color.capitalize(), self.colorMenu, checkable=True)
            colorAction.setData(color)
            _ = colorGroup.addAction(colorAction)
            _ = self.colorMenu.addAction(colorAction)
            if currentColor == color:
                colorAction.setChecked(True)
        colorGroup.setExclusive(True)
        _ = colorGroup.triggered.connect(self.changeColor)
        _ = viewMenu.addMenu(self.colorMenu)
        _ = self.menuBar().addMenu(viewMenu)

        # About menu
        aboutMenu = QMenu("&About")
        _ = aboutMenu.addAction("About &Tacty", self.showAbout)
        _ = aboutMenu.addAction("About &QT", self.showAboutQt)
        _ = self.menuBar().addMenu(aboutMenu)

    def openProject(self) -> None:
        settings = QSettings()
        url = settings.value("lastPath", type=str)
        if not isinstance(url, str):
            url = ""
        name, _ = QFileDialog.getOpenFileName(
            self, "Open project", url, "Tacty Project (*.tproj)"
        )
        if not name:
            err = QErrorMessage(self)
            err.showMessage("Could not find file.")
            return
        qInfo(f"Opening project: {name}")
        url = QFileInfo(name).canonicalPath()
        settings.setValue("lastPath", url)
        file = QFile(name)
        opened = file.open(
            QIODeviceBase.OpenModeFlag.ReadOnly | QIODeviceBase.OpenModeFlag.Text
        )
        if not opened:
            err = QErrorMessage(self)
            err.showMessage("Could not open project.")
            return
        json = bytes(file.readAll().data())
        project = Project.model_validate_json(json)
        self.showProject(project)

    def closeProject(self) -> None:
        # TODO: prompt to save if needed
        self.showWelcome()

    def newProject(self) -> None:
        modal = NewProjectModal(self)
        res = modal.exec()
        if res == QDialog.DialogCode.Rejected:
            return

        projectPath, videoPath = modal.data()

        # hash the video
        hash = getHashFromPath(videoPath)
        if hash is None:
            err = QErrorMessage(self)
            err.showMessage("Open video failed.")
            return

        # try to open the video
        vid = cv2.VideoCapture(videoPath, cv2.CAP_FFMPEG)
        fps = vid.get(cv2.CAP_PROP_FPS)
        length = int(vid.get(cv2.CAP_PROP_FRAME_COUNT))
        vid.release()

        project = Project(
            projectVersion=1,
            videoFile=videoPath,
            videoHash=hash,
            calibrationOptions=CalibrationOptions(
                videoTrim=Duration(start=0, end=length), videoFps=fps
            ),
        )

        json = project.model_dump_json()
        file = QFile(projectPath)
        opened = file.open(
            QIODeviceBase.OpenModeFlag.NewOnly | QIODeviceBase.OpenModeFlag.WriteOnly
        )
        if not opened:
            err = QErrorMessage(self)
            err.showMessage("Open project failed. Perhaps the file already exists?")
            return
        written = file.write(json.encode("utf-8"))
        if written == -1:
            err = QErrorMessage(self)
            err.showMessage("Write failed.")
            return
        file.close()
        qInfo(f"New project created: {projectPath}")
        self.showProject(project)

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
            "description": "Tacty is an open source tactile interaction analysis toolkit.",
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
