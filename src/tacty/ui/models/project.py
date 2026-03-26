from pydantic import BaseModel

from tacty.ui.utils.conversions import mmToInch


class Duration(BaseModel):
    start: int
    end: int


class Size(BaseModel):
    w: int
    h: int


class Point(BaseModel):
    x: int
    y: int

    def toString(self) -> str:
        return f"({self.x}, {self.y})"


class Corners(BaseModel):
    tl: Point | None = None
    tr: Point | None = None
    bl: Point | None = None
    br: Point | None = None

    def isValid(self):
        return self.tl and self.tr and self.bl and self.br


class CalibrationOptions(BaseModel):
    videoTrim: Duration
    videoFps: float
    videoRotation: int = 0  # 0-3, increments of 90
    videoCrop: Corners | None = None
    pageSize: Size | None = None
    processingDpi: int = 92  # 92 DPI for A3 is around FHD

    def processingResolution(self) -> Size:
        if self.pageSize is None:
            raise Exception("Called processingResolution without checking isValid")
        w = int(mmToInch(self.pageSize.w) * self.processingDpi)
        h = int(mmToInch(self.pageSize.h) * self.processingDpi)
        return Size(w=w, h=h)

    def isValid(self) -> bool:
        if not self.videoCrop or not self.videoCrop.isValid():
            return False
        return True


class Project(BaseModel):
    projectVersion: int
    videoFile: str
    videoHash: str
    calibrationOptions: CalibrationOptions
