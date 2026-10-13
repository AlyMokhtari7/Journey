from typing import Any

import pandas as pd
import sqlalchemy as sa

from journey.backend.intermediate_artifacts import DataSet
from journey.backend.RDB import (
    RDB,  # todo: INVESTIGATE: this should come from the utils ?
)
from journey.sdk.base import NodeModel


class SelectData(NodeModel):

    def execute(self, context: dict[str, Any], utils) -> sa.Select:

        sa_engine = context['sa_engine']
        sa_metaData = context['sa_metadata']
        table_name = context['table_name']
        columns = context['columns']

        if not table_name:
            utils.set_error(err_msg='table_name is required', node_name='DB')
            raise ValueError('table_name is required')

        query = RDB.select(
            table_name, *columns, engine=sa_engine, metadata=sa_metaData
        )
        print(query)
        print(table_name, columns)

        utils.log(log_msg='Finished_Selecting_Data', node_name='DB')
        return query

class ExecuteQuery(NodeModel):

    def execute(self, context: dict[str, Any], utils) -> Any:
        query = context['query']
        result = RDB.execute(query, engine=context['sa_engine'])
        return DataSet(pd.DataFrame(result))
