from typing import cast

import cv2
import pandas as pd
from cv2.typing import MatLike

from tacty.models.project import CalibrationOptions, Point
from tacty.utils.cvConversions import toSpace


class TrackingDisplayPipeline:
    data: pd.DataFrame | None
    calibration_options: CalibrationOptions

    def __init__(
        self, data: pd.DataFrame | None, calibration_options: CalibrationOptions
    ):
        self.data = data
        self.calibration_options = calibration_options

    def process(self, img: MatLike, frame: int) -> MatLike:
        if self.data is None:
            return img

        markers = self.data.loc[frame]

        if markers is None:
            return img

        canvas = img.copy()

        sides = ["left", "right"]
        fingers = ["Thumb", "Index", "Middle", "Ring", "Pinky", "Palm"]

        combinations = [(s, f) for s in sides for f in fingers]

        for side, finger in combinations:
            marker = markers[side + finger]

            if pd.isna(marker["x"]) or pd.isna(marker["y"]):
                continue

            # bounds rendering
            tl = toSpace(
                Point(x=marker["_bounds_topleft_x"], y=marker["_bounds_topleft_y"]),
                self.calibration_options.pageSize,
                self.calibration_options.processingResolution(),
            )
            br = toSpace(
                Point(
                    x=marker["_bounds_bottomright_x"], y=marker["_bounds_bottomright_y"]
                ),
                self.calibration_options.pageSize,
                self.calibration_options.processingResolution(),
            )

            _ = cv2.rectangle(
                canvas,
                tl.toCv(),
                br.toCv(),
                (255, 255, 255),
                2,
            )

            # finger - palm line rendering
            if finger != "Palm":
                palmMarker = markers[side + "Palm"]

                if pd.isna(palmMarker["x"]) or pd.isna(palmMarker["y"]):
                    continue

                fingerCenter = toSpace(
                    Point(x=marker["x"], y=marker["y"]),
                    self.calibration_options.pageSize,
                    self.calibration_options.processingResolution(),
                )

                palmCenter = toSpace(
                    Point(x=palmMarker["x"], y=palmMarker["y"]),
                    self.calibration_options.pageSize,
                    self.calibration_options.processingResolution(),
                )

                _ = cv2.line(
                    canvas,
                    fingerCenter.toCv(),
                    palmCenter.toCv(),
                    (255, 255, 255),
                    1,
                )

        return canvas
