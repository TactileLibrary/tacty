import sys

from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication

import tacty.resources.resources_rc  # pyright: ignore[reportUnusedImport, reportMissingTypeStubs] # noqa: F401

from .ui.views.main_window import MainWindow


def main() -> None:
    # Set up the application details.
    app = QApplication(sys.argv)
    app.setApplicationName("tacty")
    app.setApplicationVersion("0.1.0")
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
