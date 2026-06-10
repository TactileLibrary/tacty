from PySide6.QtCore import QCryptographicHash, QFile, QIODeviceBase


def getHashFromFile(file: QFile) -> str:
    file_size = file.size()
    sample_size = 10 * 1024 * 1024  # 10MB
    hash = QCryptographicHash(QCryptographicHash.Algorithm.Blake2b_256)

    if file_size <= sample_size * 2:
        _ = hash.addData(file)
    else:
        hash.addData(file.read(sample_size))
        _ = file.seek(file_size - sample_size)
        hash.addData(file.read(sample_size))
    hash.addData(str(file_size).encode("utf-8"))
    return bytes(hash.result().toHex().data()).decode("utf-8")


def getHashFromPath(filePath: str) -> str | None:
    file = QFile(filePath)
    if file.open(QIODeviceBase.OpenModeFlag.ReadOnly):
        return getHashFromFile(file)
    return None
