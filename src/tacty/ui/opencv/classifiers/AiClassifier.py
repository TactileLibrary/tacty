from typing import cast, override

import cv2
import numpy as np
from cv2.typing import MatLike
from onnxruntime.capi.onnxruntime_inference_collection import (  # pyright: ignore [reportMissingTypeStubs]
    InferenceSession,
)
from PySide6.QtCore import QFile, QIODeviceBase

from tacty.ui.opencv.classifiers.BaseClassifier import BaseClassifier


class AiClassifier(BaseClassifier):
    session: InferenceSession

    def __init__(self):
        model_file = QFile(":/onnx/tacty-ai-classifier-v1-0-circle-1-square.onnx")

        if not model_file.open(QIODeviceBase.OpenModeFlag.ReadOnly):
            raise FileNotFoundError("Could not find the model file in Qt resources.")

        model_bytes = bytes(model_file.readAll().data())
        model_file.close()

        self.session = InferenceSession(model_bytes)

    @override
    def pred(self, image: MatLike) -> tuple[str, float]:
        h: int
        w: int
        h, w = image.shape[:2]  # pyright: ignore [reportAny]

        if h > 20 or w > 20:
            # scale down the image
            processed = cv2.resize(image, (20, 20), interpolation=cv2.INTER_AREA)
        else:
            processed = np.zeros((20, 20), dtype=np.uint8)
            # just center the image
            y_offset = (20 - h) // 2
            x_offset = (20 - w) // 2
            processed[y_offset : y_offset + h, x_offset : x_offset + w] = image

        normalize = processed.astype(np.float32) / 255.0

        tensor = normalize[np.newaxis, np.newaxis, :, :]

        outputs = self.session.run(None, {"input": tensor})

        probabilities = cast(np.ndarray, outputs[0])[0]

        labelIdx = np.argmax(probabilities)
        confidence: float = probabilities[labelIdx]

        print("Confidence", confidence)

        if labelIdx == 0:
            label = "Circle"
        else:
            label = "Square"

        return label, confidence

    @override
    def getName(self) -> str:
        return "AI Classifier"
