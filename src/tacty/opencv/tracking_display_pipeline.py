import cv2
from cv2.typing import MatLike

from tacty.models.project import Project
from tacty.utils.cvConversions import toSpace


class TrackingDisplayPipeline:
    data: Project

    def __init__(self, data: Project):
        self.data = data

    def process(self, img: MatLike) -> MatLike:
        markers = self.data.trackingData.get(self.data.frame)

        if markers is None:
            return img

        canvas = img.copy()

        fingerToMarker: dict[str, str] = (
            self.data.trackingOptions.fingerMapping.model_dump()
        )
        markerToFinger: dict[str, str] = {m: f for f, m in fingerToMarker.items()}

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

            associated_finger = markerToFinger[key]

            if associated_finger.startswith("left"):
                associated_palm = fingerToMarker.get("leftPalm")
                if not associated_palm:
                    continue
                if associated_palm:
                    palmMarker = markers.get(associated_palm)
                    if not palmMarker:
                        continue

                    fingerCenter = toSpace(
                        marker.centroid,
                        self.data.calibrationOptions.pageSize,
                        self.data.calibrationOptions.processingResolution(),
                    )

                    palmCenter = toSpace(
                        palmMarker.centroid,
                        self.data.calibrationOptions.pageSize,
                        self.data.calibrationOptions.processingResolution(),
                    )

                    _ = cv2.line(
                        canvas,
                        fingerCenter.toCv(),
                        palmCenter.toCv(),
                        (255, 255, 255),
                        1,
                    )

            if associated_finger.startswith("right"):
                associated_palm = fingerToMarker.get("rightPalm")
                if not associated_palm:
                    continue
                if associated_palm:
                    palmMarker = markers.get(associated_palm)
                    if not palmMarker:
                        continue

                    fingerCenter = toSpace(
                        marker.centroid,
                        self.data.calibrationOptions.pageSize,
                        self.data.calibrationOptions.processingResolution(),
                    )

                    palmCenter = toSpace(
                        palmMarker.centroid,
                        self.data.calibrationOptions.pageSize,
                        self.data.calibrationOptions.processingResolution(),
                    )

                    _ = cv2.line(
                        canvas,
                        fingerCenter.toCv(),
                        palmCenter.toCv(),
                        (255, 255, 255),
                        1,
                    )

        return canvas
