import sys
from importlib.metadata import PackageNotFoundError, version

from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication

import tacty.resources.resources_rc  # pyright: ignore[reportUnusedImport, reportMissingTypeStubs] # noqa: F401

from .ui.views.main_window import MainWindow


def main() -> None:
    # Get the version from pyproject.toml.
    try:
        app_version = version("tacty")
    except PackageNotFoundError:
        app_version = "0.0.0-dev"

    # Set up the application details.
    app = QApplication(sys.argv)
    app.setApplicationName("tacty")
    app.setApplicationVersion(app_version)
    app.setDesktopFileName("net.tactilelibrary.tacty")
    app.setApplicationDisplayName(f"Tacty v{app.applicationVersion()}")
    app.setWindowIcon(QIcon(":icons/tl.svg"))
    app.setOrganizationDomain("tactilelibrary.net")
    app.setOrganizationName("TactileLibrary")

    # Load the main window.
    main_window = MainWindow()
    main_window.show()

    # Run the program.
    _ = app.exec()
