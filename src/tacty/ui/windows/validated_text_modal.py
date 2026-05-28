from PySide6.QtGui import QValidator
from PySide6.QtWidgets import QDialog, QDialogButtonBox, QLineEdit, QVBoxLayout, QWidget


class ValidatedInputDialog(QDialog):
    input: QLineEdit
    button_box: QDialogButtonBox

    def __init__(
        self, title: str, validator: QValidator, parent: QWidget | None = None
    ):
        super().__init__(parent)

        # Set properties.
        self.setModal(True)
        self.setMinimumWidth(400)
        self.setWindowTitle(title)

        layout = QVBoxLayout(self)

        self.input = QLineEdit()
        self.input.setValidator(validator)
        layout.addWidget(self.input)

        self.button_box = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel,
            self,
        )
        _ = self.button_box.accepted.connect(self.accept)
        _ = self.button_box.rejected.connect(self.reject)
        layout.addWidget(self.button_box)

        # Validate on every keystroke to toggle the OK button state
        _ = self.input.textChanged.connect(self.check_validation)
        self.check_validation()

    def check_validation(self) -> None:
        ok_button = self.button_box.button(QDialogButtonBox.StandardButton.Ok)
        if ok_button:
            ok_button.setEnabled(self.input.hasAcceptableInput())

    def textValue(self) -> str:
        return self.input.text()

    @staticmethod
    def getText(
        title: str, validator: QValidator, parent: QWidget | None = None
    ) -> str | None:
        dialog = ValidatedInputDialog(title, validator, parent)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            return dialog.textValue()
        return None
