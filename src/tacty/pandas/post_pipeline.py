from typing import cast

import pandas as pd

from tacty.models.project import Project


class PostProcessingPipeline:
    project: Project

    def __init__(self, project: Project):
        self.project = project

    def processs(self):
        df = self.loadDataframe()

    def loadDataframe(self) -> pd.DataFrame:
        # transforming the TrackingData into a dict that contains another dict, with a tuple as key
        rows = {
            outer_key: {
                (inner_key, "x"): tp.centroid.x for inner_key, tp in inner_dict.items()
            }
            | {(inner_key, "y"): tp.centroid.y for inner_key, tp in inner_dict.items()}
            for outer_key, inner_dict in self.project.trackingData.items()
        }

        # make that tuple a multiindex
        df = pd.DataFrame.from_dict(rows, orient="index").sort_index()  # pyright: ignore [reportUnknownMemberType]
        df.columns = pd.MultiIndex.from_tuples(df.columns)
        df = df.sort_index(axis=1, level=[0, 1])

        # rename the columns to the finger names
        mapping = self.project.trackingOptions.fingerMapping.toInverseDict()
        columns = cast(list[tuple[str, str]], list(df.columns))
        df.columns = pd.MultiIndex.from_tuples(
            [
                (mapped, col[1])
                for col in columns
                if (mapped := mapping.get(col[0])) is not None
            ]
        )

        print(df.head())
        print(df.shape)

        return df
