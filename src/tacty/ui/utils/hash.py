from PySide6.QtCore import QCryptographicHash, QFile, QIODeviceBase


def getHashFromFile(file: QFile) -> str:
    hash = QCryptographicHash(QCryptographicHash.Algorithm.Sha256)
    _ = hash.addData(file)
    return bytes(hash.result().toHex().data()).decode("utf-8")


def getHashFromPath(filePath: str) -> str | None:
    file = QFile(filePath)
    if file.open(QIODeviceBase.OpenModeFlag.ReadOnly):
        return getHashFromFile(file)
    return None
