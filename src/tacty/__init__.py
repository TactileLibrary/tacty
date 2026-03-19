import sys
from importlib.metadata import PackageNotFoundError, version

from PySide6.QtCore import QFile, QIODevice, QSettings, Qt, QTextStream
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication, QStyleFactory

import tacty.resources.resources_rc  # pyright: ignore[reportUnusedImport] # noqa: F401
import tacty.resources.themes.breeze_pyside6  # pyright: ignore[reportUnusedImport] # noqa: F401

from .ui.windows import MainWindow


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
    app.setStyle(QStyleFactory.create("Fusion"))
    if QSettings().value("lightMode", type=bool):
        file = QFile(":/light/stylesheet.qss")
        _ = file.open(QIODevice.OpenModeFlag.ReadOnly | QIODevice.OpenModeFlag.Text)
        stream = QTextStream(file)
        app.setStyleSheet(stream.readAll())
    else:
        app.styleHints().setColorScheme(Qt.ColorScheme.Dark)
        file = QFile(":/dark/stylesheet.qss")
        _ = file.open(QIODevice.OpenModeFlag.ReadOnly | QIODevice.OpenModeFlag.Text)
        stream = QTextStream(file)
        app.setStyleSheet(stream.readAll())

    # Load the main window.
    main_window = MainWindow()
    main_window.show()

    # Run the program.
    _ = app.exec()
