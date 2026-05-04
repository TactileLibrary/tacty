from time import time
from typing import cast, override
from warnings import deprecated

import cv2
import numpy as np
from cv2.typing import MatLike
from PySide6.QtCore import QThread, Signal

from tacty.models.project import BoundingBox, Point, Project, TrackedMarker
from tacty.opencv.calibration_pipeline import CalibrationPipeline
from tacty.opencv.classifiers.AiClassifier import AiClassifier
from tacty.opencv.classifiers.BaseClassifier import BaseClassifier
from tacty.opencv.classifiers.HuMomentsClassifier import HuMomentsClassifier
from tacty.utils.cvConversions import toSpace


class TrackingPipeline(QThread):
    project: Project

    debugImages: dict[str, MatLike]

    progress: Signal = Signal(int)

    classifier: BaseClassifier | None = None

    def __init__(self, project: Project, debugImages: dict[str, MatLike]):
        super().__init__()
        self.project = project
        self.debugImages = debugImages

    def mapToMask(self, img: MatLike, tolerance: float = 0.25) -> MatLike:
        _, max_val, _, _ = cv2.minMaxLoc(img)

        tolerance = int(max(max_val, 5) * tolerance)

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
        if self.classifier is None:
            return

        idx1, idx2 = indices[0], indices[1]

        x1, y1 = stats[idx1, cv2.CC_STAT_LEFT], stats[idx1, cv2.CC_STAT_TOP]
        w1, h1 = stats[idx1, cv2.CC_STAT_WIDTH], stats[idx1, cv2.CC_STAT_HEIGHT]
        cropped_labels1 = labels[y1 : y1 + h1, x1 : x1 + w1]
        target_label1 = np.array([idx1], dtype=np.int32)

        mask1 = cv2.inRange(cropped_labels1, target_label1, target_label1)

        x2, y2 = stats[idx2, cv2.CC_STAT_LEFT], stats[idx2, cv2.CC_STAT_TOP]
        w2, h2 = stats[idx2, cv2.CC_STAT_WIDTH], stats[idx2, cv2.CC_STAT_HEIGHT]
        cropped_labels = labels[y2 : y2 + h2, x2 : x2 + w2]
        target_label = np.array([idx2], dtype=np.int32)

        mask2 = cv2.inRange(cropped_labels, target_label, target_label)

        label1, conf1 = self.classifier.pred(mask1)

        label2, conf2 = self.classifier.pred(mask2)

        if label1 == label2:
            if conf1 > conf2:
                # flip label 2
                if label2 == "Square":
                    label2 = "Circle"
                else:
                    label2 = "Square"
            else:
                # flip label 1
                if label1 == "Square":
                    label1 = "Circle"
                else:
                    label1 = "Square"

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
        if self.classifier is None:
            return

        x, y = stats[index, cv2.CC_STAT_LEFT], stats[index, cv2.CC_STAT_TOP]
        w, h = stats[index, cv2.CC_STAT_WIDTH], stats[index, cv2.CC_STAT_HEIGHT]
        cropped_labels = labels[y : y + h, x : x + w]
        target_label = np.array([index], dtype=np.int32)

        mask = cv2.inRange(cropped_labels, target_label, target_label)

        label, _ = self.classifier.pred(mask)

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

    @deprecated(
        "Extremely slow due to repeated arithmetics. Use getFastColorMap() and precomputeLuts() instead."
    )
    def getColorMap(self, h: MatLike, sv: MatLike, target_hue: int, width: int = 15):
        diff = np.abs(h - target_hue)
        dist = np.minimum(diff, 180 - diff)

        hue_score = np.maximum(0, 1 - (dist / width))

        color_map = hue_score * sv

        return (color_map * 255).astype(np.uint8)

    def getFastColorMap(self, h: MatLike, sv: MatLike, lut: np.ndarray):
        hue_score = cv2.LUT(h, lut)
        return cv2.multiply(hue_score, sv, scale=1.0 / 255.0, dtype=cv2.CV_8U)

    def precomputeLuts(self, width: int = 15) -> dict[str, np.ndarray]:
        luts: dict[str, np.ndarray] = {}

        targets = {
            "r": self.project.trackingOptions.hues.r,
            "g": self.project.trackingOptions.hues.g,
            "b": self.project.trackingOptions.hues.b,
            "c": self.project.trackingOptions.hues.c,
            "y": self.project.trackingOptions.hues.y,
            "m": self.project.trackingOptions.hues.m,
        }

        for key, target_hue in targets.items():
            lut = np.zeros((256, 1), dtype=np.uint8)
            hue_values = np.arange(180)

            diff = np.abs(hue_values - target_hue)
            dist = np.minimum(diff, 180 - diff)
            hue_score = (np.maximum(0, 1 - (dist / width)) * 255).astype(np.uint8)

            lut[:180, 0] = hue_score
            luts[key] = lut

        return luts

    def updateDebugImages(self, image: MatLike):
        # image is already calibrated

        hsv_img = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        h, s, v = cv2.split(hsv_img)

        lower_hsv = np.array([0, 50, 50], dtype=np.uint8)
        upper_hsv = np.array([180, 255, 255], dtype=np.uint8)
        sv_mask = cv2.inRange(hsv_img, lower_hsv, upper_hsv)
        sv_base = cv2.multiply(s, v, scale=1.0 / 255.0)
        sv = cv2.bitwise_and(sv_base, sv_mask)

        luts = self.precomputeLuts()

        r_map = self.getFastColorMap(h, sv, luts["r"])
        g_map = self.getFastColorMap(h, sv, luts["g"])
        b_map = self.getFastColorMap(h, sv, luts["b"])
        c_map = self.getFastColorMap(h, sv, luts["c"])
        y_map = self.getFastColorMap(h, sv, luts["y"])
        m_map = self.getFastColorMap(h, sv, luts["m"])

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

        # prepare a classifier
        if self.project.trackingOptions.classifier == "hu":
            self.classifier = HuMomentsClassifier()
        if self.project.trackingOptions.classifier == "ai":
            self.classifier = AiClassifier()

        if self.classifier is None:
            return
        print(f"Starting tracking using the {self.classifier.getName()} classifier.")

        # seek to start frame
        frame = self.project.calibrationOptions.videoTrim.start.value
        _ = video.set(cv2.CAP_PROP_POS_FRAMES, frame)

        timeDecoding: float = 0
        timeCalibration: float = 0
        timeHSV: float = 0
        timeMap: float = 0
        timeMask: float = 0
        timeTrack: float = 0

        luts = self.precomputeLuts()

        while frame <= self.project.calibrationOptions.videoTrim.end.value:
            if self.isInterruptionRequested():
                break  # if the user clicks cancel

            t1 = time()
            success, img = video.read()
            if not success:
                continue
            t2 = time()
            timeDecoding += t2 - t1

            calibrated_img = calibration.process(img)
            t3 = time()
            timeCalibration += t3 - t2

            hsv_img = cv2.cvtColor(calibrated_img, cv2.COLOR_BGR2HSV)
            h, s, v = cv2.split(hsv_img)
            t4 = time()
            timeHSV = t4 - t3

            # changed this to CV math for better performance
            lower_hsv = np.array([0, 50, 50], dtype=np.uint8)
            upper_hsv = np.array([180, 255, 255], dtype=np.uint8)
            sv_mask = cv2.inRange(hsv_img, lower_hsv, upper_hsv)
            sv_base = cv2.multiply(s, v, scale=1.0 / 255.0)
            sv = cv2.bitwise_and(sv_base, sv_mask)

            r_map = self.getFastColorMap(h, sv, luts["r"])
            g_map = self.getFastColorMap(h, sv, luts["g"])
            b_map = self.getFastColorMap(h, sv, luts["b"])
            c_map = self.getFastColorMap(h, sv, luts["c"])
            y_map = self.getFastColorMap(h, sv, luts["y"])
            m_map = self.getFastColorMap(h, sv, luts["m"])
            t5 = time()
            timeMap += t5 - t4

            r_mask = self.mapToMask(r_map, self.project.trackingOptions.tolerances.r)
            g_mask = self.mapToMask(g_map, self.project.trackingOptions.tolerances.g)
            b_mask = self.mapToMask(b_map, self.project.trackingOptions.tolerances.b)
            c_mask = self.mapToMask(c_map, self.project.trackingOptions.tolerances.c)
            y_mask = self.mapToMask(y_map, self.project.trackingOptions.tolerances.y)
            m_mask = self.mapToMask(m_map, self.project.trackingOptions.tolerances.m)
            t6 = time()
            timeMask += t6 - t5

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
            t7 = time()
            timeTrack += t7 - t6

            self.project.trackingData[frame] = markers

            self.progress.emit(frame)
            print("Processed frame", frame)
            frame += 1

        # close the video
        video.release()

        # release memory
        self.classifier = None

        # print profiler
        print(
            f"Time spent: decoding {timeDecoding}s, calibrating {timeCalibration}s, transforming to HSV {timeHSV}s, extracting color maps {timeMap}s, computing masks {timeMask}s and tracking the fingers {timeTrack}s."
        )

        self.finished.emit()
