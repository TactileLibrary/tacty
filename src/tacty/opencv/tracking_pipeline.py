from time import time
from typing import override

import cv2
import numpy as np
from cv2.typing import MatLike
from PySide6.QtCore import QThread, Signal
from typing_extensions import deprecated

from tacty.models.project import BoundingBox, Point, Project, TrackedMarker
from tacty.opencv.calibration_pipeline import CalibrationPipeline
from tacty.opencv.preprocessing_pipeline import PreProcessingPipeline
from tacty.opencv.classifiers.AiClassifier import AiClassifier
from tacty.opencv.classifiers.BaseClassifier import BaseClassifier
from tacty.opencv.classifiers.HuMomentsClassifier import HuMomentsClassifier
from tacty.utils.cvConversions import toSpace


class TrackingPipeline(QThread):
    project: Project

    debugImages: dict[str, MatLike]

    progress: Signal = Signal(int)

    classifier: BaseClassifier | None = None

    calibration: CalibrationPipeline
    preprocessing: PreProcessingPipeline

    def __init__(self, project: Project, debugImages: dict[str, MatLike]):
        super().__init__()
        self.project = project
        self.debugImages = debugImages
        self.calibration = CalibrationPipeline(project.calibrationOptions)
        self.preprocessing = PreProcessingPipeline(project.preProcessingOptions, project.videoFile)

    def mapToMask(self, img: MatLike, tolerance: float = 0.25) -> MatLike:
        max_val = 255  # logic moved to map generation

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
        c = Point(x=round(centroids[index][0]), y=round(centroids[index][1]))  # pyright: ignore [reportAny]
        cs = toSpace(
            c,
            self.project.calibrationOptions.processingResolution(),
            self.project.calibrationOptions.pageSize,
        )
        tl = Point(
            x=round(stats[index][cv2.CC_STAT_LEFT]),  # pyright: ignore [reportAny]
            y=round(stats[index][cv2.CC_STAT_TOP]),  # pyright: ignore [reportAny]
        )
        tls = toSpace(
            tl,
            self.project.calibrationOptions.processingResolution(),
            self.project.calibrationOptions.pageSize,
        )
        br = Point(
            x=tl.x + round(stats[index][cv2.CC_STAT_WIDTH]),  # pyright: ignore [reportAny]
            y=tl.y + round(stats[index][cv2.CC_STAT_HEIGHT]),  # pyright: ignore [reportAny]
        )
        brs = toSpace(
            br,
            self.project.calibrationOptions.processingResolution(),
            self.project.calibrationOptions.pageSize,
        )

        markers[color + label] = TrackedMarker(
            centroid=cs, bounds=BoundingBox(tl=tls, br=brs)
        )

    def cleanMask(self, img: MatLike):
        height = img.shape[0]
        scale = height / 1000  # around the default of 92 DPI on A3
        open_base = 3
        close_base = 5

        # compute kernel sizes to use
        open_size = max(open_base, int(open_base * scale))
        if open_size % 2 == 0:
            open_size += 1
        close_size = max(close_base, int(close_base * scale))
        if close_size % 2 == 0:
            close_size += 1

        # create the kernels
        kernel_open = cv2.getStructuringElement(cv2.MORPH_RECT, (open_size, open_size))
        kernel_close = cv2.getStructuringElement(
            cv2.MORPH_RECT, (close_size, close_size)
        )

        # open to remove specks
        img_cleaned = cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel_open)
        # close to fill gaps
        img_cleaned = cv2.morphologyEx(img_cleaned, cv2.MORPH_CLOSE, kernel_close)

        return img_cleaned

    def findMarkers(
        self, img: MatLike, color: str, markers: dict[str, TrackedMarker]
    ) -> None:
        count, labels, stats, centroids = cv2.connectedComponentsWithStats(
            img, connectivity=8
        )

        if count <= 1:
            return

        areas = stats[1:, cv2.CC_STAT_AREA]
        sorted_offsets = np.argsort(areas)[::-1]
        sorted_indices = sorted_offsets + 1
        top_indices = [
            idx for idx in sorted_indices if stats[idx, cv2.CC_STAT_AREA] > 25
        ]

        if len(top_indices) >= 2:
            # found both markers
            self.classifyTwoMarkers(
                labels, stats, centroids, color, markers, np.array(top_indices)
            )
            return

        if len(top_indices) == 1:
            # found one marker
            self.classifyOneMarker(
                labels, stats, centroids, color, markers, top_indices[0]
            )
            return

    @deprecated(
        "Extremely slow due to repeated arithmetics. Use getFastColorMap() and precomputeLuts() instead."
    )
    def getColorMap(self, h: MatLike, sv: MatLike, target_hue: int, width: int = 10):
        diff = np.abs(h - target_hue)
        dist = np.minimum(diff, 180 - diff)

        hue_score = np.maximum(0, 1 - (dist / width))

        color_map = hue_score * sv

        return (color_map * 255).astype(np.uint8)

    def getFastColorMap(
        self, h: MatLike, sv: MatLike, lut: np.ndarray, debug: str = ""
    ):
        hue_score = cv2.LUT(h, lut)
        if debug != "":
            self.debugImages[debug + " hue difference"] = hue_score
        color_map = cv2.multiply(hue_score, sv, scale=1.0 / 255.0, dtype=cv2.CV_8U)

        _, max_val, _, _ = cv2.minMaxLoc(color_map)

        if max_val < 20:
            return np.zeros_like(color_map)

        return cv2.normalize(color_map, color_map, 0, 255, cv2.NORM_MINMAX)

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
        if "Original" in self.debugImages:
            # show the preprocessed image
            self.debugImages["Preprocessed"] = self.preprocessing.process(self.debugImages["Original"])

        # image is already calibrated

        self.debugImages["Calibrated"] = image
        hsv_img = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        h, s, v = cv2.split(hsv_img)

        lower_hsv = np.array([0, 50, 50], dtype=np.uint8)
        upper_hsv = np.array([180, 255, 255], dtype=np.uint8)
        sv_mask = cv2.inRange(hsv_img, lower_hsv, upper_hsv)
        sv_base = cv2.multiply(s, v, scale=1.0 / 255.0)
        sv = cv2.bitwise_and(sv_base, sv_mask)

        self.debugImages["Hue"] = h
        self.debugImages["Saturation"] = s
        self.debugImages["Value"] = v
        self.debugImages["SV base"] = sv_base
        self.debugImages["SV factor"] = sv

        luts = self.precomputeLuts()

        r_map = self.getFastColorMap(h, sv, luts["r"], debug="red")
        g_map = self.getFastColorMap(h, sv, luts["g"], debug="green")
        b_map = self.getFastColorMap(h, sv, luts["b"], debug="blue")
        c_map = self.getFastColorMap(h, sv, luts["c"], debug="cyan")
        y_map = self.getFastColorMap(h, sv, luts["y"], debug="yellow")
        m_map = self.getFastColorMap(h, sv, luts["m"], debug="magenta")

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

        r_mask_clean = self.cleanMask(r_mask)
        g_mask_clean = self.cleanMask(g_mask)
        b_mask_clean = self.cleanMask(b_mask)
        c_mask_clean = self.cleanMask(c_mask)
        y_mask_clean = self.cleanMask(y_mask)
        m_mask_clean = self.cleanMask(m_mask)

        self.debugImages["Red clean mask"] = r_mask_clean
        self.debugImages["green clean mask"] = g_mask_clean
        self.debugImages["Blue clean mask"] = b_mask_clean
        self.debugImages["Cyan clean mask"] = c_mask_clean
        self.debugImages["Yellow clean mask"] = y_mask_clean
        self.debugImages["Magenta clean mask"] = m_mask_clean

    @override
    def run(self):
        # open the video
        video = cv2.VideoCapture(self.project.videoFile, cv2.CAP_FFMPEG)
        video.setExceptionMode(True)

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
        timeClean: float = 0
        timePreprocessing: float = 0

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

            preprocessed_img = self.preprocessing.process(img)
            t3 = time()
            timePreprocessing += t3 - t2
            
            calibrated_img = self.calibration.process(preprocessed_img)
            t4 = time()
            timeCalibration += t4 - t3

            hsv_img = cv2.cvtColor(calibrated_img, cv2.COLOR_BGR2HSV)
            h, s, v = cv2.split(hsv_img)
            t5 = time()
            timeHSV = t5 - t4   

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
            t6 = time()
            timeMap += t6 - t5

            r_mask = self.mapToMask(r_map, self.project.trackingOptions.tolerances.r)
            g_mask = self.mapToMask(g_map, self.project.trackingOptions.tolerances.g)
            b_mask = self.mapToMask(b_map, self.project.trackingOptions.tolerances.b)
            c_mask = self.mapToMask(c_map, self.project.trackingOptions.tolerances.c)
            y_mask = self.mapToMask(y_map, self.project.trackingOptions.tolerances.y)
            m_mask = self.mapToMask(m_map, self.project.trackingOptions.tolerances.m)
            t7 = time()
            timeMask += t7 - t6

            r_mask_clean = self.cleanMask(r_mask)
            g_mask_clean = self.cleanMask(g_mask)
            b_mask_clean = self.cleanMask(b_mask)
            c_mask_clean = self.cleanMask(c_mask)
            y_mask_clean = self.cleanMask(y_mask)
            m_mask_clean = self.cleanMask(m_mask)
            t8 = time()
            timeClean += t8 - t7

            markers: dict[str, TrackedMarker] = {}

            self.findMarkers(r_mask_clean, "red", markers)
            self.findMarkers(g_mask_clean, "green", markers)
            self.findMarkers(b_mask_clean, "blue", markers)
            self.findMarkers(c_mask_clean, "cyan", markers)
            self.findMarkers(y_mask_clean, "yellow", markers)
            self.findMarkers(m_mask_clean, "magenta", markers)
            t9 = time()
            timeTrack += t9 - t8

            self.project.trackingData[frame] = markers

            self.progress.emit(frame)
            frame += 1

        # close the video
        video.release()

        # release memory
        self.classifier = None

        # print profiler
        print(
            f"Time spent: decoding {timeDecoding}s, calibrating {timeCalibration}s, transforming to HSV {timeHSV}s, extracting color maps {timeMap}s, computing masks {timeMask}s, cleaning the masks {timeClean}s and tracking the fingers {timeTrack}s."
        )

        self.finished.emit()
