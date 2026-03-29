from pydantic import BaseModel

from tacty.ui.utils.unitConversions import mmToInch


class Value[T](BaseModel):
    value: T
    default: T


class Duration(BaseModel):
    start: Value[int]
    end: Value[int]


class Size(BaseModel):
    w: int
    h: int

    def toString(self) -> str:
        return f"{self.w}x{self.h}"


class Point(BaseModel):
    x: int
    y: int

    def toString(self) -> str:
        return f"({self.x}, {self.y})"


class Corners(BaseModel):
    tl: Value[Point]
    tr: Value[Point]
    bl: Value[Point]
    br: Value[Point]


class CalibrationOptions(BaseModel):
    videoTrim: Duration
    videoFps: Value[float]
    videoFrameCount: int
    videoRotation: int = 0  # 0-3, increments of 90
    videoCrop: Corners
    pageSize: Size = Size(w=420, h=297)
    processingDpi: int = 92  # 92 DPI for A3 is around FHD

    def processingResolution(self) -> Size:
        w = int(mmToInch(self.pageSize.w) * self.processingDpi)
        h = int(mmToInch(self.pageSize.h) * self.processingDpi)
        return Size(w=w, h=h)


class Project(BaseModel):
    projectVersion: int
    videoFile: str
    videoHash: str
    frame: int = 0
    calibrationOptions: CalibrationOptions
