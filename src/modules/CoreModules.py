from modules.sklearn import BaseResult

from typing import Any

import pandas as pd

from journey.backend.intermediate_artifacts import DataBundle, DataSet
from journey.sdk.base import NodeModel


class ShowDataFrameInfo(NodeModel):

    def execute(self, context: dict[str, Any], utils) -> None:
        artifact = context["data_frame"]

        if isinstance(artifact, DataSet):
            dataframes = {"data": artifact.data}

        elif isinstance(artifact, DataBundle):
            dataframes = {
                **artifact.features,
                **artifact.target,
            }

        else:
            raise TypeError(
                f"Expected DataSet or DataBundle, "
                f"got {artifact}"
                f"got {type(artifact).__name__}"
            )

        for name, df in dataframes.items():
            print(f"\n{'-' * 10} {name} Info {'-' * 10}")
            df.info()

            print(f"{'-' * 10} {name} Head {'-' * 10}")
            print(df.head())

        utils.log(
            log_msg="Finished_Display_Data",
            node_name="Core",
        )
