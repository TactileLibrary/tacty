from typing import override

import cv2
from cv2.typing import MatLike
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
    QWidget,
)

from tacty.models.project import (
    CalibrationOptions,
    Corners,
    Duration,
    Point,
    Project,
    Value,
)
from tacty.ui.views import ProjectView, WelcomeView
from tacty.ui.windows.image_viewer_popup import ImageViewerPopup
from tacty.ui.windows.new_project_modal import NewProjectModal
from tacty.utils.hash import getHashFromPath


class MainWindow(QMainWindow):
    # Signals
    themeChanged: Signal = Signal()

    # Dynamic menus
    saveAction: QAction
    saveAsAction: QAction
    closeAction: QAction
    colorMenu: QMenu
    debugImagesMenu: QMenu
    debugEnabled: QAction

    # Debug
    debugImages: dict[str, MatLike] = {}

    # Data
    currentWidget: QWidget
    openedFile: str | None

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

        self.openedFile = None
        self.currentWidget = welcomeView

        self.saveAction.setEnabled(False)
        self.saveAsAction.setEnabled(False)
        self.closeAction.setEnabled(False)

    def showProject(self, project: Project):
        projectView = ProjectView(project, self.debugImages)

        self.setCentralWidget(projectView)
        _ = projectView.debugChanged.connect(self.updateDebugImages)

        self.currentWidget = projectView

        self.saveAction.setEnabled(True)
        self.saveAsAction.setEnabled(True)
        self.closeAction.setEnabled(True)

    def initMenuBar(self) -> None:
        # File menu
        fileMenu = QMenu("&File")
        _ = fileMenu.addAction("&New", "Ctrl+N", self.newProject)
        _ = fileMenu.addAction("&Open", "Ctrl+O", self.openProject)
        _ = fileMenu.addSeparator()
        self.saveAction = fileMenu.addAction(
            "&Save project", "Ctrl+S", self.saveProject
        )
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

        # Debug menu
        debugMenu = QMenu("&Debug")
        self.debugEnabled = QAction(text="Enable", checkable=True)
        _ = self.debugEnabled.toggled.connect(self.toggleDebug)
        debugMenu.addAction(self.debugEnabled)
        self.debugImagesMenu = QMenu("&Images")
        self.debugImagesMenu.setDisabled(True)
        _ = debugMenu.addMenu(self.debugImagesMenu)
        _ = self.menuBar().addMenu(debugMenu)

        # About menu
        aboutMenu = QMenu("&About")
        _ = aboutMenu.addAction("About &Tacty", self.showAbout)
        _ = aboutMenu.addAction("About &QT", self.showAboutQt)
        _ = self.menuBar().addMenu(aboutMenu)

    def updateDebugImages(self) -> None:
        self.debugImagesMenu.clear()

        for name in self.debugImages:
            _ = self.debugImagesMenu.addAction(
                name, lambda n=name: self.displayImg(n, self.debugImages[n])
            )

    def toggleDebug(self, enabled: bool) -> None:
        if isinstance(self.currentWidget, ProjectView):
            self.currentWidget.debugMode = enabled

        if enabled:
            self.debugImagesMenu.setDisabled(False)
            return
        self.debugImagesMenu.setDisabled(True)

    def displayImg(self, name: str, image: MatLike) -> None:
        dialog = ImageViewerPopup(name, image)
        _ = dialog.exec()

    def openProject(self) -> None:
        settings = QSettings()
        url = settings.value("lastPath", type=str)
        if not isinstance(url, str):
            url = ""
        name, _ = QFileDialog.getOpenFileName(
            self, "Open project", url, "Tacty Project (*.tproj)"
        )
        if not name:
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
        hash = getHashFromPath(project.videoFile)
        if project.videoHash != hash:
            err = QErrorMessage(self)
            err.showMessage(
                "Video file changed. Please restore the original file, or create a new project."
            )
            return
        self.openedFile = name
        self.showProject(project)

    def closeProject(self) -> bool:
        confirm = QMessageBox.warning(
            self,
            "Close project?",
            "Any unsaved changes will be lost.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No,
        )
        if confirm == QMessageBox.StandardButton.Yes:
            self.showWelcome()
            return True
        return False

    def saveProject(self) -> None:
        if not isinstance(self.currentWidget, ProjectView) or self.openedFile is None:
            err = QErrorMessage(self)
            err.showMessage("Cannot save, no project open.")
            return

        project = self.currentWidget.project

        json = project.model_dump_json()
        file = QFile(self.openedFile)
        opened = file.open(QIODeviceBase.OpenModeFlag.WriteOnly)
        if not opened:
            err = QErrorMessage(self)
            err.showMessage("Save project failed, cannot open file.")
            return
        written = file.write(json.encode("utf-8"))
        if written == -1:
            err = QErrorMessage(self)
            err.showMessage("Write failed.")
            return
        file.close()
        qInfo(f"Project saved: {self.openedFile}")

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
        count = int(vid.get(cv2.CAP_PROP_FRAME_COUNT))
        length = int(vid.get(cv2.CAP_PROP_FRAME_COUNT)) - 1  # frames are 0-indexed
        width = int(vid.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(vid.get(cv2.CAP_PROP_FRAME_HEIGHT))
        vid.release()

        project = Project(
            projectVersion=1,
            videoFile=videoPath,
            videoHash=hash,
            calibrationOptions=CalibrationOptions(
                videoTrim=Duration(
                    start=Value[int](value=0, default=0),
                    end=Value[int](value=length, default=length),
                ),
                videoFps=Value[float](value=fps, default=fps),
                videoFrameCount=count,
                videoCrop=Corners(
                    tl=Value[Point](value=Point(x=0, y=0), default=Point(x=0, y=0)),
                    tr=Value[Point](
                        value=Point(x=width, y=0), default=Point(x=width, y=0)
                    ),
                    bl=Value[Point](
                        value=Point(x=0, y=height), default=Point(x=0, y=height)
                    ),
                    br=Value[Point](
                        value=Point(x=width, y=height), default=Point(x=width, y=height)
                    ),
                ),
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
        self.openedFile = projectPath
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
