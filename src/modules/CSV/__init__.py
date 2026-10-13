from typing import Any

import pandas as pd

from journey.backend.intermediate_artifacts import DataSet
from journey.sdk.base import NodeModel


class ReadCSV(NodeModel):

    def verify_ui_context(self, ui_context: dict[str, Any],) -> bool:
            if not isinstance(ui_context, dict):
                return False

            file_name = ui_context.get("file_name")

            return isinstance(file_name, str) and bool(file_name.strip())

    def execute(self, context: dict[str, Any], utils) -> DataSet:
        if not self.verify_ui_context(context):
            utils.set_error(err_msg='File_Name_Invalid', node_name='CSV')
            raise ValueError(
                "Invalid configuration: 'file_name' "
                "must be a non-empty string."
            )

        file_path = context['file_name']

        df = pd.read_csv(file_path)
        utils.log(log_msg='Finished_Reading_CSV', node_name='CSV')
        return DataSet(df)
