from typing import Any

import pandas as pd

from journey.sdk.base import NodeModel


class ShowDataFrameInfo(NodeModel):

    def execute(self, context: dict[str, Any], utils) -> None:

        df: pd.DataFrame = context['data_frame'].data

        print("-" * 10 + "DataFrame Info" + "-" * 10)
        df.info()
        print("-" * 10 + "DataFrame Head" + "-" * 10)
        print(df.head())

        utils.log(log_msg='Finished_Display_Data', node_name='Core')
