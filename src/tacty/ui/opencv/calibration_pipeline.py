import cv2
import numpy as np
from cv2.typing import MatLike

from tacty.ui.models.project import CalibrationOptions


class CalibrationPipeline:
    options: CalibrationOptions

    def __init__(self, options: CalibrationOptions):
        self.options = options

    def process(self, img: MatLike) -> MatLike:
        height: int
        width: int
        height, width = img.shape[:2]  # pyright: ignore [reportAny] have to do thiss due to C bindings

        srcPoints = np.array(
            [
                [self.options.videoCrop.tl.value.x, self.options.videoCrop.tl.value.y],
                [self.options.videoCrop.tr.value.x, self.options.videoCrop.tr.value.y],
                [self.options.videoCrop.br.value.x, self.options.videoCrop.br.value.y],
                [self.options.videoCrop.bl.value.x, self.options.videoCrop.bl.value.y],
            ],
            dtype=np.float32,
        )

        dstPoints = np.array(
            [
                [0.0, 0.0],  # Top-Left
                [width, 0.0],  # Top-Right
                [width, height],  # Bottom-Right
                [0.0, height],  # Bottom-Left
            ],
            dtype=np.float32,
        )

        warped = cv2.getPerspectiveTransform(srcPoints, dstPoints)
        return cv2.warpPerspective(img, warped, (width, height))
