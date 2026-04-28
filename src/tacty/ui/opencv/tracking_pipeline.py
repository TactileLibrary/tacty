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

    debugImages: dict[str, MatLike]

    progress: Signal = Signal(int)

    def __init__(self, project: Project, debugImages: dict[str, MatLike]):
        super().__init__()
        self.project = project
        self.debugImages = debugImages

    def mapToMask(self, img: MatLike, tolerance: float = 0.25) -> MatLike:
        _, max_val, _, _ = cv2.minMaxLoc(img)

        tolerance = int(max_val * tolerance)

        lower_bound = np.array([max_val - tolerance])
        upper_bound = np.array([max_val])

        return cv2.inRange(img, lower_bound, upper_bound)

    def classifyTwoMarkers(
        self,
        labels: MatLike,
        stats: MatLike,
        centroids: MatLike,
        color: str,
        markers: dict[str, TrackedMarker],
        indices: np.ndarray,
    ) -> None:
        idx1, idx2 = indices[0], indices[1]

        mask1 = cast(np.ndarray, (labels == idx1).astype(np.uint8) * 255)  # pyright: ignore [reportAny]
        mask2 = cast(np.ndarray, (labels == idx2).astype(np.uint8) * 255)  # pyright: ignore [reportAny]

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
        c1 = Point(x=round(centroids[idx1][0]), y=round(centroids[idx1][1]))  # pyright: ignore [reportAny]
        c1s = toSpace(
            c1,
            self.project.calibrationOptions.processingResolution(),
            self.project.calibrationOptions.pageSize,
        )
        c2 = Point(x=round(centroids[idx2][0]), y=round(centroids[idx2][1]))  # pyright: ignore [reportAny]
        c2s = toSpace(
            c2,
            self.project.calibrationOptions.processingResolution(),
            self.project.calibrationOptions.pageSize,
        )
        tl1 = Point(
            x=round(stats[idx1][cv2.CC_STAT_LEFT]),  # pyright: ignore [reportAny]
            y=round(stats[idx1][cv2.CC_STAT_TOP]),  # pyright: ignore [reportAny]
        )
        tl1s = toSpace(
            tl1,
            self.project.calibrationOptions.processingResolution(),
            self.project.calibrationOptions.pageSize,
        )
        br1 = Point(
            x=tl1.x + round(stats[idx1][cv2.CC_STAT_WIDTH]),  # pyright: ignore [reportAny]
            y=tl1.y + round(stats[idx1][cv2.CC_STAT_HEIGHT]),  # pyright: ignore [reportAny]
        )
        br1s = toSpace(
            br1,
            self.project.calibrationOptions.processingResolution(),
            self.project.calibrationOptions.pageSize,
        )
        tl2 = Point(
            x=round(stats[idx2][cv2.CC_STAT_LEFT]),  # pyright: ignore [reportAny]
            y=round(stats[idx2][cv2.CC_STAT_TOP]),  # pyright: ignore [reportAny]
        )
        tl2s = toSpace(
            tl2,
            self.project.calibrationOptions.processingResolution(),
            self.project.calibrationOptions.pageSize,
        )
        br2 = Point(
            x=tl2.x + round(stats[idx2][cv2.CC_STAT_WIDTH]),  # pyright: ignore [reportAny]
            y=tl2.y + round(stats[idx2][cv2.CC_STAT_HEIGHT]),  # pyright: ignore [reportAny]
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
        c = Point(x=round(centroids[1][0]), y=round(centroids[1][1]))  # pyright: ignore [reportAny]
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

    def getColorMap(
        self, h: MatLike, s: MatLike, v: MatLike, target_hue: int, width: int = 15
    ):
        diff = np.abs(h - target_hue)
        dist = np.minimum(diff, 180 - diff)

        hue_score = np.maximum(0, 1 - (dist / width))

        color_map = hue_score * (s / 255.0) * (v / 255.0)

        color_map[s < 50] = 0
        color_map[v < 50] = 0

        return (color_map * 255).astype(np.uint8)

    def updateDebugImages(self, image: MatLike):
        # image is already calibrated

        hsv_img = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        hsv_img_float = hsv_img.astype(np.float32)
        h, s, v = cv2.split(hsv_img_float)

        r_map = self.getColorMap(h, s, v, self.project.trackingOptions.hues.r)
        g_map = self.getColorMap(h, s, v, self.project.trackingOptions.hues.g)
        b_map = self.getColorMap(h, s, v, self.project.trackingOptions.hues.b)
        c_map = self.getColorMap(h, s, v, self.project.trackingOptions.hues.c)
        y_map = self.getColorMap(h, s, v, self.project.trackingOptions.hues.y)
        m_map = self.getColorMap(h, s, v, self.project.trackingOptions.hues.m)

        self.debugImages["Red map"] = r_map
        self.debugImages["Green map"] = g_map
        self.debugImages["Blue map"] = b_map
        self.debugImages["Cyan map"] = c_map
        self.debugImages["Yellow map"] = y_map
        self.debugImages["Magenta map"] = m_map

        r_mask = self.mapToMask(r_map, self.project.trackingOptions.tolerances.r)
        g_mask = self.mapToMask(g_map, self.project.trackingOptions.tolerances.g)
        b_mask = self.mapToMask(b_map, self.project.trackingOptions.tolerances.b)
        c_mask = self.mapToMask(c_map, self.project.trackingOptions.tolerances.c)
        y_mask = self.mapToMask(y_map, self.project.trackingOptions.tolerances.y)
        m_mask = self.mapToMask(m_map, self.project.trackingOptions.tolerances.m)

        self.debugImages["Red mask"] = r_mask
        self.debugImages["Green mask"] = g_mask
        self.debugImages["Blue mask"] = b_mask
        self.debugImages["Cyan mask"] = c_mask
        self.debugImages["Yellow mask"] = y_mask
        self.debugImages["Magenta mask"] = m_mask

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

            hsv_img = cv2.cvtColor(calibrated_img, cv2.COLOR_BGR2HSV)
            hsv_img_float = hsv_img.astype(np.float32)
            h, s, v = cv2.split(hsv_img_float)

            r_map = self.getColorMap(h, s, v, self.project.trackingOptions.hues.r)
            g_map = self.getColorMap(h, s, v, self.project.trackingOptions.hues.g)
            b_map = self.getColorMap(h, s, v, self.project.trackingOptions.hues.b)
            c_map = self.getColorMap(h, s, v, self.project.trackingOptions.hues.c)
            y_map = self.getColorMap(h, s, v, self.project.trackingOptions.hues.y)
            m_map = self.getColorMap(h, s, v, self.project.trackingOptions.hues.m)

            r_mask = self.mapToMask(r_map, self.project.trackingOptions.tolerances.r)
            g_mask = self.mapToMask(g_map, self.project.trackingOptions.tolerances.g)
            b_mask = self.mapToMask(b_map, self.project.trackingOptions.tolerances.b)
            c_mask = self.mapToMask(c_map, self.project.trackingOptions.tolerances.c)
            y_mask = self.mapToMask(y_map, self.project.trackingOptions.tolerances.y)
            m_mask = self.mapToMask(m_map, self.project.trackingOptions.tolerances.m)

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
