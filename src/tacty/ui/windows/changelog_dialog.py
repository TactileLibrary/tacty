from PySide6.QtCore import QFile, QIODevice, QTextStream
from PySide6.QtWidgets import QDialog, QTextBrowser, QVBoxLayout, QWidget


class ChangelogDialog(QDialog):
    def __init__(self, parent: QWidget | None = None):
        super().__init__(parent)

        # set properties
        self.setWindowTitle("Changelog")
        self.resize(500, 500)

        # load the changelog
        changelog_file = QFile(":/CHANGELOG.md")
        _ = changelog_file.open(
            QIODevice.OpenModeFlag.ReadOnly | QIODevice.OpenModeFlag.Text
        )
        changelog = QTextStream(changelog_file).readAll()
        changelog_file.close()

        # process the changelog to remove the foreward
        changelog_stripped = "## [" + changelog.split("## [", 1)[1]

        # display it
        layout = QVBoxLayout(self)
        text_browser = QTextBrowser()
        text_browser.setMarkdown(changelog_stripped)
        layout.addWidget(text_browser)

    @staticmethod
    def showChangelog() -> None:
        dialog = ChangelogDialog()
        _ = dialog.exec()
