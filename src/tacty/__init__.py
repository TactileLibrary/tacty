import sys
from importlib.metadata import PackageNotFoundError, version

from PySide6.QtCore import QSettings, Qt
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication, QStyleFactory

import tacty.resources.resources_rc  # pyright: ignore[reportUnusedImport, reportMissingTypeStubs] # noqa: F401

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
        app.styleHints().setColorScheme(Qt.ColorScheme.Light)
    else:
        app.styleHints().setColorScheme(Qt.ColorScheme.Dark)

    # Load the main window.
    main_window = MainWindow()
    main_window.show()

    # Run the program.
    _ = app.exec()
