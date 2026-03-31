import cv2
from cv2.typing import MatLike

from tacty.ui.models.project import Project
from tacty.ui.utils.cvConversions import toSpace


class TrackingDisplayPipeline:
    data: Project

    def __init__(self, data: Project):
        self.data = data

    def process(self, img: MatLike) -> MatLike:
        markers = self.data.trackingData.get(self.data.frame)

        if markers is None:
            return img

        canvas = img.copy()

        for key in markers:
            marker = markers[key]

            tl = toSpace(
                marker.bounds.tl,
                self.data.calibrationOptions.pageSize,
                self.data.calibrationOptions.processingResolution(),
            )
            br = toSpace(
                marker.bounds.br,
                self.data.calibrationOptions.pageSize,
                self.data.calibrationOptions.processingResolution(),
            )

            _ = cv2.rectangle(
                canvas,
                tl.toCv(),
                br.toCv(),
                (255, 255, 255),
                2,
            )

            _ = cv2.putText(
                canvas, key, tl.toCv(), cv2.FONT_HERSHEY_PLAIN, 1, (255, 255, 255)
            )

        return canvas
