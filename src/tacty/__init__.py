import sys
from importlib.metadata import PackageNotFoundError, version

from PySide6.QtCore import QFile, QIODevice, QSettings, QTextStream
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication, QStyleFactory

import tacty.resources.resources_rc  # pyright: ignore[reportUnusedImport] # noqa: F401
import tacty.resources.themes.breeze_pyside6  # pyright: ignore[reportUnusedImport] # noqa: F401

from .ui.windows import MainWindow

default_style: str
main_window: MainWindow | None = None


def main() -> None:
    # Get the version from pyproject.toml.
    try:
        app_version = version("tacty")
    except PackageNotFoundError:
        app_version = "0.0.0"

    # Set up the application details.
    app = QApplication(sys.argv)
    app.setApplicationName("tacty")
    app.setApplicationVersion(app_version)
    app.setDesktopFileName("net.tactilelibrary.tacty")
    app.setApplicationDisplayName("Tacty")
    app.setWindowIcon(QIcon(":icons/tl.svg"))
    app.setOrganizationDomain("tactilelibrary.net")
    app.setOrganizationName("TactileLibrary")

    # Load the theme
    global default_style
    default_style = app.style().objectName()
    loadTheme(app)

    # Load the main window.
    global main_window
    main_window = MainWindow()
    main_window.show()

    # Connect signals
    _ = main_window.themeChanged.connect(lambda: loadTheme(app))

    # Run the program.
    _ = app.exec()


def loadTheme(app: QApplication):
    settings = QSettings()
    settings.beginGroup("appearance")
    theme = settings.value("theme", type=str) or "dark"
    color = settings.value("color", type=str) or "blue"
    settings.endGroup()
    global main_window
    if theme == "native":
        app.setStyle(QStyleFactory.create(default_style))
        app.setStyleSheet("")
        if main_window:
            main_window.colorMenu.setEnabled(False)
        return
    app.setStyle(QStyleFactory.create("Fusion"))
    file = QFile(f":/{theme}-{color}/stylesheet.qss")
    _ = file.open(QIODevice.OpenModeFlag.ReadOnly | QIODevice.OpenModeFlag.Text)
    stream = QTextStream(file)
    app.setStyleSheet(stream.readAll())
    if main_window:
        main_window.colorMenu.setEnabled(True)
