from enum import Enum
from typing import Annotated, Generic, TypeVar

import cv2
import numpy as np
from pydantic import BaseModel, Field
from typing_extensions import Literal

from tacty.utils.unitConversions import mmToInch

T = TypeVar("T")


class Value(BaseModel, Generic[T]):
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


class ColorOptions(BaseModel, Generic[T]):
    r: T
    y: T
    g: T
    c: T
    b: T
    m: T


class FingerMapping(BaseModel):
    leftThumb: str | None = "cyanCircle"
    leftIndex: str | None = "yellowCircle"
    leftMiddle: str | None = "blueCircle"
    leftRing: str | None = "greenCircle"
    leftPinky: str | None = "redCircle"
    leftPalm: str | None = "magentaCircle"
    rightThumb: str | None = "cyanSquare"
    rightIndex: str | None = "yellowSquare"
    rightMiddle: str | None = "blueSquare"
    rightRing: str | None = "greenSquare"
    rightPinky: str | None = "redSquare"
    rightPalm: str | None = "magentaSquare"

    def toDict(self) -> dict[str, str]:
        return self.model_dump()

    def toInverseDict(self) -> dict[str, str]:
        dictionary = self.toDict()
        inverse = {v: k for k, v in dictionary.items()}
        return inverse


class TrackingOptions(BaseModel):
    hues: ColorOptions[int] = ColorOptions(r=0, y=30, g=60, c=90, b=120, m=150)
    tolerances: ColorOptions[float] = ColorOptions(
        r=0.25, y=0.25, g=0.25, c=0.25, b=0.25, m=0.25
    )
    fingerMapping: FingerMapping = FingerMapping()
    classifier: str = "hu"


class AOIType(str, Enum):
    RECTANGLE = "rectangle"
    POLYGON = "polygon"


class AOIBase(BaseModel):
    name: str


class AOIRect(AOIBase):
    type: Literal[AOIType.RECTANGLE] = AOIType.RECTANGLE
    tl: Point
    br: Point

    def test(self, other: Point) -> bool:
        return (
            other.x >= self.tl.x
            and other.x <= self.br.x
            and other.y >= self.tl.y
            and other.y <= self.br.y
        )


class AOIPoly(AOIBase):
    type: Literal[AOIType.POLYGON] = AOIType.POLYGON
    points: list[Point]

    def test(self, other: Point) -> bool:
        contour = np.array([p.toCv() for p in self.points], dtype=np.int32).reshape(
            (-1, 1, 2)
        )

        return cv2.pointPolygonTest(contour, other.toCv(), measureDist=False) >= 0


AOI = Annotated[AOIRect | AOIPoly, Field(discriminator="type")]


class PostProcessingOptions(BaseModel):
    speedOutlier: bool = True
    anatomyOutlier: bool = True
    interpolation: bool = True
    interpolationLimit: float = 0.0
    aois: list[AOI] = []


class Project(BaseModel):
    projectVersion: int
    videoFile: str
    videoHash: str
    frame: int = 0
    calibrationOptions: CalibrationOptions
    trackingOptions: TrackingOptions = TrackingOptions()
    postProcessingOptions: PostProcessingOptions = PostProcessingOptions()
    trackingData: dict[int, dict[str, TrackedMarker]] = {}
