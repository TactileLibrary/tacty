from typing import override

from PySide6.QtGui import QValidator
from PySide6.QtWidgets import QWidget


class AOINameValidator(QValidator):
    used_set: set[str]

    def __init__(self, forbidden_list: list[str], parent: QWidget | None = None):
        super().__init__(parent)
        # items should already be stripped, but we do it again just in case
        self.used_set = {item.strip().lower() for item in forbidden_list}

    @override
    def validate(self, text: str, pos: int):
        # comas are fully invalid, you should not be allowed to press them
        if "," in text:
            return QValidator.State.Invalid, text, pos

        # for already used names we use intermediate, so the user can still change it
        cleaned_text = text.strip().lower()
        if not cleaned_text or cleaned_text in self.used_set:
            return QValidator.State.Intermediate, text, pos

        return QValidator.State.Acceptable, text, pos
