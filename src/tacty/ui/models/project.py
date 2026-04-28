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

    def toCv(self) -> tuple[int, int]:
        return (self.x, self.y)


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

    def maxDpi(self) -> int:
        # phsyical size - inch
        pw = mmToInch(self.pageSize.w)
        ph = mmToInch(self.pageSize.h)

        # video size - px
        vw = self.videoCrop.tr.default.x
        vh = self.videoCrop.bl.default.y

        # max dpi per axis
        mrw = int(vw / pw)
        mrh = int(vh / ph)

        return min(mrw, mrh)


class BoundingBox(BaseModel):
    tl: Point
    br: Point


class TrackedMarker(BaseModel):
    centroid: Point
    bounds: BoundingBox


class ColorOptions[T](BaseModel):
    r: T
    y: T
    g: T
    c: T
    b: T
    m: T


class FingerMapping(BaseModel):
    leftThumb: str = "cyanCircle"
    leftIndex: str = "yellowCircle"
    leftMiddle: str = "blueCircle"
    leftRing: str = "greenCircle"
    leftPinky: str = "redCircle"
    leftPalm: str = "magentaCircle"
    rightThumb: str = "cyanSquare"
    rightIndex: str = "yellowSquare"
    rightMiddle: str = "blueSquare"
    rightRing: str = "greenSquare"
    rightPinky: str = "redSquare"
    rightPalm: str = "magentaSquare"


class TrackingOptions(BaseModel):
    hues: ColorOptions[int] = ColorOptions(r=0, y=30, g=60, c=90, b=120, m=150)
    tolerances: ColorOptions[float] = ColorOptions(
        r=0.25, y=0.25, g=0.25, c=0.25, b=0.25, m=0.25
    )
    fingerMapping: FingerMapping = FingerMapping()


class Project(BaseModel):
    projectVersion: int
    videoFile: str
    videoHash: str
    frame: int = 0
    calibrationOptions: CalibrationOptions
    trackingOptions: TrackingOptions = TrackingOptions()
    trackingData: dict[int, dict[str, TrackedMarker]] = {}
