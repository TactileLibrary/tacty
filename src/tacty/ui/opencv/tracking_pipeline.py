from typing import cast, override

import cv2
import numpy as np
from cv2.typing import MatLike
from PySide6.QtCore import QThread, Signal

from tacty.ui.models.project import BoundingBox, Point, Project, TrackedMarker
from tacty.ui.opencv.calibration_pipeline import CalibrationPipeline
from tacty.ui.utils.cvConversions import toSpace


class TrackingPipeline(QThread):
    project: Project

    progress: Signal = Signal(int)

    def __init__(self, project: Project):
        super().__init__()
        self.project = project

    def mapToMask(self, img: MatLike, tolerance: int = 25) -> MatLike | None:
        _, max_val, _, _ = cv2.minMaxLoc(img)

        tolerance = int(max_val * tolerance / 100)

        lower_bound = np.array([max_val - tolerance])
        upper_bound = np.array([max_val])

        if max_val > 30:
            return cv2.inRange(img, lower_bound, upper_bound)
        return None

    def classifyTwoMarkers(
        self,
        labels: MatLike,
        stats: MatLike,
        centroids: MatLike,
        color: str,
        markers: dict[str, TrackedMarker],
        indices: np.ndarray,
    ) -> None:
        mask1 = cast(np.ndarray, (labels == indices[0]).astype(np.uint8) * 255)  # pyright: ignore [reportAny]
        mask2 = cast(np.ndarray, (labels == indices[1]).astype(np.uint8) * 255)  # pyright: ignore [reportAny]

        # find contours
        countour1 = cv2.findContours(mask1, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)[
            0
        ][0]
        countour2 = cv2.findContours(mask2, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)[
            0
        ][0]

        # get the area
        area1 = cv2.contourArea(countour1)
        area2 = cv2.contourArea(countour2)

        # fitting elipse
        _, axes1, _ = cv2.fitEllipse(countour1)
        _, axes2, _ = cv2.fitEllipse(countour2)
        area_e1 = (np.pi * axes1[0] * axes1[1]) / 4
        area_e2 = (np.pi * axes2[0] * axes2[1]) / 4
        ratio_e1 = area1 / area_e1
        ratio_e2 = area2 / area_e2

        # fitting rectangle
        rect1 = cv2.minAreaRect(countour1)
        rect2 = cv2.minAreaRect(countour2)
        area_r1 = rect1[1][0] * rect1[1][1]
        area_r2 = rect2[1][0] * rect2[1][1]
        ratio_r1 = area1 / area_r1
        ratio_r2 = area2 / area_r2

        circleness_1 = ratio_e1 - ratio_r1
        circleness_2 = ratio_e2 - ratio_r2

        if circleness_1 > circleness_2:
            label1 = "Circle"
            label2 = "Square"
        else:
            label1 = "Square"
            label2 = "Circle"

        # get data in physical space
        c1 = Point(x=round(centroids[1][0]), y=round(centroids[1][0]))  # pyright: ignore [reportAny]
        c1s = toSpace(
            c1,
            self.project.calibrationOptions.processingResolution(),
            self.project.calibrationOptions.pageSize,
        )
        c2 = Point(x=round(centroids[2][0]), y=round(centroids[2][0]))  # pyright: ignore [reportAny]
        c2s = toSpace(
            c2,
            self.project.calibrationOptions.processingResolution(),
            self.project.calibrationOptions.pageSize,
        )
        tl1 = Point(
            x=round(stats[1][cv2.CC_STAT_LEFT]),  # pyright: ignore [reportAny]
            y=round(stats[1][cv2.CC_STAT_TOP]),  # pyright: ignore [reportAny]
        )
        tl1s = toSpace(
            tl1,
            self.project.calibrationOptions.processingResolution(),
            self.project.calibrationOptions.pageSize,
        )
        br1 = Point(
            x=tl1.x + round(stats[1][cv2.CC_STAT_WIDTH]),  # pyright: ignore [reportAny]
            y=tl1.y + round(stats[1][cv2.CC_STAT_HEIGHT]),  # pyright: ignore [reportAny]
        )
        br1s = toSpace(
            br1,
            self.project.calibrationOptions.processingResolution(),
            self.project.calibrationOptions.pageSize,
        )
        tl2 = Point(
            x=round(stats[2][cv2.CC_STAT_LEFT]),  # pyright: ignore [reportAny]
            y=round(stats[2][cv2.CC_STAT_TOP]),  # pyright: ignore [reportAny]
        )
        tl2s = toSpace(
            tl2,
            self.project.calibrationOptions.processingResolution(),
            self.project.calibrationOptions.pageSize,
        )
        br2 = Point(
            x=tl2.x + round(stats[2][cv2.CC_STAT_WIDTH]),  # pyright: ignore [reportAny]
            y=tl2.y + round(stats[2][cv2.CC_STAT_HEIGHT]),  # pyright: ignore [reportAny]
        )
        br2s = toSpace(
            br2,
            self.project.calibrationOptions.processingResolution(),
            self.project.calibrationOptions.pageSize,
        )

        markers[color + label1] = TrackedMarker(
            centroid=c1s, bounds=BoundingBox(tl=tl1s, br=br1s)
        )
        markers[color + label2] = TrackedMarker(
            centroid=c2s, bounds=BoundingBox(tl=tl2s, br=br2s)
        )

    def classifyOneMarker(
        self,
        labels: MatLike,
        stats: MatLike,
        centroids: MatLike,
        color: str,
        markers: dict[str, TrackedMarker],
        index: int,
    ) -> None:
        mask = cast(np.ndarray, (labels == index).astype(np.uint8) * 255)  # pyright: ignore [reportAny]

        # find contours
        countour = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)[0][
            0
        ]

        # get the area
        area = cv2.contourArea(countour)

        # circularity calculation
        peri = cv2.arcLength(countour, True)
        circularity = (4 * np.pi * area) / (peri**2)

        # fitting rectangle
        rect = cv2.minAreaRect(countour)
        area_r = rect[1][0] * rect[1][1]
        ratio_r = area / area_r

        if circularity > ratio_r:
            label = "Circle"
        else:
            label = "Square"

        # get data in physical space
        c = Point(x=round(centroids[1][0]), y=round(centroids[1][0]))  # pyright: ignore [reportAny]
        cs = toSpace(
            c,
            self.project.calibrationOptions.processingResolution(),
            self.project.calibrationOptions.pageSize,
        )
        tl = Point(
            x=round(stats[1][cv2.CC_STAT_LEFT]),  # pyright: ignore [reportAny]
            y=round(stats[1][cv2.CC_STAT_TOP]),  # pyright: ignore [reportAny]
        )
        tls = toSpace(
            tl,
            self.project.calibrationOptions.processingResolution(),
            self.project.calibrationOptions.pageSize,
        )
        br = Point(
            x=tl.x + round(stats[1][cv2.CC_STAT_WIDTH]),  # pyright: ignore [reportAny]
            y=tl.y + round(stats[1][cv2.CC_STAT_HEIGHT]),  # pyright: ignore [reportAny]
        )
        brs = toSpace(
            br,
            self.project.calibrationOptions.processingResolution(),
            self.project.calibrationOptions.pageSize,
        )

        markers[color + label] = TrackedMarker(
            centroid=cs, bounds=BoundingBox(tl=tls, br=brs)
        )

    def findMarkers(
        self, img: MatLike, color: str, markers: dict[str, TrackedMarker]
    ) -> None:
        count, labels, stats, centroids = cv2.connectedComponentsWithStats(
            img, connectivity=8
        )

        areas = stats[1:, cv2.CC_STAT_AREA]
        top_indices = np.argsort(areas)[::-1][:2] + 1

        if count > 2 and stats[top_indices[1]][cv2.CC_STAT_AREA] > 25:
            # found both markers
            self.classifyTwoMarkers(
                labels, stats, centroids, color, markers, top_indices
            )
            return

        if count == 2 and stats[top_indices[0]][cv2.CC_STAT_AREA] > 25:
            # found one marker
            self.classifyOneMarker(
                labels, stats, centroids, color, markers, top_indices[0]
            )
            return

    @override
    def run(self):
        # open the video
        video = cv2.VideoCapture(self.project.videoFile, cv2.CAP_FFMPEG)
        video.setExceptionMode(True)

        # prepare a calibrationPipeline
        calibration = CalibrationPipeline(self.project.calibrationOptions)

        # seek to start frame
        frame = self.project.calibrationOptions.videoTrim.start.value
        _ = video.set(cv2.CAP_PROP_POS_FRAMES, frame)

        while frame <= self.project.calibrationOptions.videoTrim.end.value:
            if self.isInterruptionRequested():
                break  # if the user clicks cancel

            success, img = video.read()
            if not success:
                continue

            calibrated_img = calibration.process(img)

            b, g, r = cv2.split(calibrated_img)

            r_map = cv2.subtract(cv2.subtract(r, g), b)  # r - g - b
            g_map = cv2.subtract(cv2.subtract(g, b), r)  # g - b - r
            b_map = cv2.subtract(cv2.subtract(b, r), g)  # b - r - g

            c_map = cv2.subtract(cv2.min(b, g), r)  # min(b,g) - r
            y_map = cv2.subtract(cv2.min(g, r), b)  # min(g,r) - b
            m_map = cv2.subtract(cv2.min(b, r), g)  # min(b,r) - g

            r_mask = self.mapToMask(r_map)
            g_mask = self.mapToMask(g_map)
            b_mask = self.mapToMask(b_map)
            c_mask = self.mapToMask(c_map)
            y_mask = self.mapToMask(y_map)
            m_mask = self.mapToMask(m_map)

            markers: dict[str, TrackedMarker] = {}

            if r_mask is not None:
                self.findMarkers(r_mask, "red", markers)
            if g_mask is not None:
                self.findMarkers(g_mask, "green", markers)
            if b_mask is not None:
                self.findMarkers(b_mask, "blue", markers)
            if c_mask is not None:
                self.findMarkers(c_mask, "cyan", markers)
            if y_mask is not None:
                self.findMarkers(y_mask, "yellow", markers)
            if m_mask is not None:
                self.findMarkers(m_mask, "magenta", markers)

            self.project.trackingData[frame] = markers

            self.progress.emit(frame)
            print("Processed frame", frame)
            frame += 1

        # close the video
        video.release()

        self.finished.emit()
