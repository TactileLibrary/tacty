from typing import cast

import cv2
import numpy as np
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

        active_markers = self.data.columns.get_level_values(0)

        for side, finger in combinations:
            finger_name = side + finger

            if finger_name not in active_markers:
                continue

            marker = markers[finger_name]

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

            # onion skin rendering, +/- 1s
            window = round(self.calibration_options.videoFps.value)
            idx_min = cast(int, self.data.index.min())
            idx_max = cast(int, self.data.index.max())
            start_frame = max(idx_min, frame - window)
            end_frame = min(idx_max, frame + window)
            window_data = self.data.loc[start_frame:end_frame, (side + finger)]
            coordinates = window_data[["x", "y"]].dropna().values.astype(float)

            if len(coordinates) > 1:
                # vectorized toSpace logic - should move to a differenf file later
                og = self.calibration_options.pageSize
                to = self.calibration_options.processingResolution()
                scales = np.array([to.w / og.w, to.h / og.h])
                scaled_pts = np.round(coordinates * scales).astype(np.int32)

                # draw line by line to have a color gradient
                pts = len(scaled_pts)
                for i in range(pts - 1):
                    pt1 = tuple(scaled_pts[i])
                    pt2 = tuple(scaled_pts[i + 1])

                    color_progress = i / (pts - 1)
                    blue = int(255 * color_progress)
                    green = 0
                    red = int(255 * (1.0 - color_progress))
                    segment_color = (blue, green, red)

                    _ = cv2.line(
                        canvas,
                        pt1,
                        pt2,
                        segment_color,
                        thickness=1,
                        lineType=cv2.LINE_AA,
                    )

            # finger - palm line rendering
            if finger != "Palm":
                palm_name = side + "Palm"

                if palm_name not in active_markers:
                    continue

                palmMarker = markers[palm_name]

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
