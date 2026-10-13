from typing import Any

from journey.backend.RDB import (
    RDB,  # todo: INVESTIGATE: this should come from the utils ?
)
from journey.sdk.base import NodeModel


class SelectData(NodeModel):

    def execute(self, context: dict[str, Any], utils) -> None:

        sa_engine = context['sa_engine']
        sa_metaData = context['sa_metadata']
        table_name = context['table_name']
        columns = context['columns']

        if table_name:
            query = RDB.select(
                table_name, *columns, engine=sa_engine, metadata=sa_metaData
            )
            print(query)
            print(table_name, columns)

            RDB.pretty_print(RDB.execute(query, sa_engine))

            utils.log(log_msg='Finished_Selecting_Data', node_name='DB')
