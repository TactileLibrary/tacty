from typing import cast

import numpy as np
import pandas as pd

from tacty.models.project import Point, Project


class PostProcessingPipeline:
    project: Project

    def __init__(self, project: Project):
        self.project = project

    def processs(self) -> pd.DataFrame:
        interpolationLimit = self.project.postProcessingOptions.interpolationLimit
        interpolationLimit = (
            round(interpolationLimit * self.project.calibrationOptions.videoFps.value)
            if interpolationLimit
            else None
        )

        df = self.loadDataframe()
        if self.project.postProcessingOptions.speedOutlier:
            self.removeSpeedOutliers(df)
        if self.project.postProcessingOptions.anatomyOutlier:
            self.removeAnatomyOutliers(df)
        if self.project.postProcessingOptions.interpolation:
            df = df.interpolate(
                method="linear", limit=interpolationLimit, limit_direction="both"
            )
        df = df.round()  # need ints

        self.addAOIs(df)  # add the AOI data

        return df.astype("Int32")

    def addAOIs(self, df: pd.DataFrame) -> None:
        aois = self.project.postProcessingOptions.aois
        if not aois:
            return

        markers = df.columns.get_level_values(0).unique()

        for marker in markers:
            if (marker, "x") not in df.columns or (marker, "y") not in df.columns:
                continue

            # extract the coordinates
            marker_x = df[(marker, "x")]
            marker_y = df[(marker, "y")]
            coords = pd.concat([marker_x, marker_y], axis=1)

            for aoi in aois:
                feature_name = f"in_{aoi.name}"

                def testAOI(row) -> int:
                    x_val, y_val = row.iloc[0], row.iloc[1]

                    # default 0 if we don't have position dataa
                    if pd.isna(x_val) or pd.isna(y_val):
                        return 0

                    pt = Point(x=x_val, y=y_val)
                    return 1 if aoi.test(pt) else 0

                df[(marker, feature_name)] = coords.apply(testAOI, axis=1)

    def removeSpeedOutliers(self, df: pd.DataFrame) -> None:
        for marker in df.columns.get_level_values(0).unique():
            # compute speed
            dx = df.loc[:, (marker, "x")].diff()
            dy = df.loc[:, (marker, "y")].diff()
            speed = np.sqrt(dx**2 + dy**2)

            # rolling IQR
            Q1 = speed.rolling(
                window=round(self.project.calibrationOptions.videoFps.value / 2.0),
                center=True,
            ).quantile(0.25)
            Q3 = speed.rolling(
                window=round(self.project.calibrationOptions.videoFps.value / 2.0),
                center=True,
            ).quantile(0.75)
            IQR = Q3 - Q1
            upper_bound = Q3 + 1.5 * IQR

            is_outlier = speed > upper_bound
            df.loc[is_outlier, (marker, slice(None))] = np.nan

    def removeAnatomyOutliers(self, df: pd.DataFrame) -> None:
        markers = df.columns.get_level_values(0).unique()

        palms = [m for m in markers if "Palm" in m]
        if not palms:
            return

        for marker in markers:
            if "Palm" in marker:
                continue

            prefix = (
                "left"
                if marker.startswith("left")
                else "right"
                if marker.startswith("right")
                else None
            )
            anchor = f"{prefix}Palm"
            if anchor not in palms:
                continue

            dx = df.loc[:, (marker, "x")] - df.loc[:, (anchor, "x")]
            dy = df.loc[:, (marker, "y")] - df.loc[:, (anchor, "y")]
            dist_to_palm = np.sqrt(dx**2 + dy**2)

            Q1 = dist_to_palm.quantile(0.25)
            Q3 = dist_to_palm.quantile(0.75)
            IQR = Q3 - Q1

            upper_limit = Q3 + 1.5 * IQR
            lower_limit = Q1 - 1.5 * IQR

            is_outlier = (dist_to_palm > upper_limit) | (dist_to_palm < lower_limit)
            df.loc[is_outlier, (marker, slice(None))] = np.nan

    def loadDataframe(self) -> pd.DataFrame:
        # transforming the TrackingData into a dict that contains another dict, with a tuple as key
        rows = {
            outer_key: {
                (inner_key, "x"): tp.centroid.x for inner_key, tp in inner_dict.items()
            }
            | {(inner_key, "y"): tp.centroid.y for inner_key, tp in inner_dict.items()}
            | {
                (inner_key, "_bounds_topleft_x"): tp.bounds.tl.x
                for inner_key, tp in inner_dict.items()
            }
            | {
                (inner_key, "_bounds_topleft_y"): tp.bounds.tl.y
                for inner_key, tp in inner_dict.items()
            }
            | {
                (inner_key, "_bounds_bottomright_x"): tp.bounds.br.x
                for inner_key, tp in inner_dict.items()
            }
            | {
                (inner_key, "_bounds_bottomright_y"): tp.bounds.br.y
                for inner_key, tp in inner_dict.items()
            }
            for outer_key, inner_dict in self.project.trackingData.items()
        }

        # make that tuple a multiindex
        df = pd.DataFrame.from_dict(rows, orient="index").sort_index()  # pyright: ignore [reportUnknownMemberType]
        df.columns = pd.MultiIndex.from_tuples(df.columns)
        df = df.sort_index(axis=1, level=[0, 1])

        # rename the columns to the finger names
        mapping = self.project.trackingOptions.fingerMapping.toInverseDict()
        valid_columns = [col for col in df.columns if mapping.get(col[0]) is not None]
        df = cast(pd.DataFrame, df[valid_columns])
        columns = cast(list[tuple[str, str]], list(df.columns))
        df.columns = pd.MultiIndex.from_tuples(
            [
                (mapped, col[1])
                for col in columns
                if (mapped := mapping.get(col[0])) is not None
            ]
        )

        return df
