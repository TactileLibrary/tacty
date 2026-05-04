from typing import override

import cv2
import numpy as np
from cv2.typing import MatLike

from tacty.opencv.classifiers.BaseClassifier import BaseClassifier


class HuMomentsClassifier(BaseClassifier):
    circleContour: MatLike
    squareContour: MatLike

    def __init__(self):
        # generate the templates
        circleCanvas = np.zeros((100, 100), dtype=np.uint8)
        squareCanvas = np.zeros((100, 100), dtype=np.uint8)

        _ = cv2.circle(circleCanvas, (50, 50), 40, 255, -1)
        _ = cv2.rectangle(squareCanvas, (10, 10), (90, 90), 255, -1)

        circleCountours, _ = cv2.findContours(
            circleCanvas, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
        )
        squareContours, _ = cv2.findContours(
            squareCanvas, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
        )

        self.circleContour = circleCountours[0]
        self.squareContour = squareContours[0]

    @override
    def getName(self) -> str:
        return "Hu Moments"

    @override
    def pred(self, image: MatLike) -> tuple[str, float]:
        # find contour
        countour = cv2.findContours(image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[
            0
        ][0]

        # match to reference shapes
        circleScore = cv2.matchShapes(
            countour, self.circleContour, cv2.CONTOURS_MATCH_I2, 0
        )
        squareScore = cv2.matchShapes(
            countour, self.squareContour, cv2.CONTOURS_MATCH_I2, 0
        )

        if circleScore < squareScore:
            label = "Circle"
        else:
            label = "Square"

        # we use diff of scores as confidence
        return label, abs(circleScore - squareScore)
