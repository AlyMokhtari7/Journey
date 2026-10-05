import inspect
import os

import sqlalchemy as sa
from dotenv import load_dotenv
from sqlalchemy import inspect
from tabulate import tabulate

# --- Env Data ---
load_dotenv()
CONNECTION_STRING = os.getenv("CONNECTION_STRING")

class RDB:

    @staticmethod
    def get_all_tables_name():   
        engine: sa.engine.Engine = sa.create_engine(str(CONNECTION_STRING)) 
        inspector = inspect(engine)

        tables = inspector.get_table_names()

        print(tables)
        return tables

    @staticmethod
    def get_column_names(table_name: str) -> list[str]:
        engine: sa.engine.Engine = sa.create_engine(str(CONNECTION_STRING))
        with engine.connect() as conn:
            result = conn.execute(sa.text(f"SELECT * FROM {table_name} LIMIT 0"))
            return list(result.keys())

    def __init__(self, connection_string: str):
        self._engine: sa.Engine = sa.create_engine(connection_string)
        self._metadata: sa.MetaData = sa.MetaData()
        self._query: sa.Select | None = None

    # ---------- Tables ----------

    def get_table(self, table_name: str) -> sa.Table:
        return sa.Table(
            table_name,
            self._metadata,
            autoload_with=self._engine
        )

    # ---------- Query construction ----------

    def select(self, table_name: str, *columns: str):
        table = self.get_table(table_name)

        if columns:
            selected_columns = [
                getattr(table.c, column)
                for column in columns
            ]
            self._query = sa.select(*selected_columns)
        else:
            self._query = sa.select(table)

        return self

    def where_clause_on_col(self, col_name: str, operator: str, value):
        if self._query is None:
            raise RuntimeError("No query has been created.")

        table = self._get_current_table()
        column = getattr(table.c, col_name)

        operators = {
            "=": column.__eq__,
            "!=": column.__ne__,
            ">": column.__gt__,
            ">=": column.__ge__,
            "<": column.__lt__,
            "<=": column.__le__,
        }

        if operator not in operators:
            raise ValueError(f"Unsupported operator: {operator}")

        condition = operators[operator](value)

        self._query = self._query.where(condition)

        return self

    def group_by(self, *columns: str):
        if self._query is None:
            raise RuntimeError("No query has been created.")

        table = self._get_current_table()

        self._query = self._query.group_by(
            *(getattr(table.c, column) for column in columns)
        )

        return self

    def having(self, condition):
        if self._query is None:
            raise RuntimeError("No query has been created.")

        self._query = self._query.having(condition)

        return self

    def order_by(self, column: str, descending: bool = False):
        if self._query is None:
            raise RuntimeError("No query has been created.")

        table = self._get_current_table()

        column_obj = getattr(table.c, column)

        if descending:
            column_obj = column_obj.desc()

        self._query = self._query.order_by(column_obj)

        return self

    def limit(self, limit: int):
        if self._query is None:
            raise RuntimeError("No query has been created.")

        self._query = self._query.limit(limit)

        return self

    def offset(self, offset: int):
        if self._query is None:
            raise RuntimeError("No query has been created.")

        self._query = self._query.offset(offset)

        return self

    # ---------- Execution ----------

    def execute(self):
        if self._query is None:
            raise RuntimeError("No query has been created.")

        with self._engine.connect() as conn:
            result = conn.execute(self._query)
            return result.fetchall()

    # ---------- Utilities ----------

    def pretty_print(self, res):
        print(tabulate(res, headers="keys", tablefmt="pretty"))

    def show_query(self):
        if self._query is None:
            raise RuntimeError("No query has been created.")

        print(self._query)

    def _get_current_table(self):
        if self._query is None:
            raise RuntimeError("No query has been created.")

        # Get the first FROM clause
        froms = self._query.get_final_froms()

        if not froms:
            raise RuntimeError("Query has no table.")

        return froms[0]

def main():
    rdb = RDB(CONNECTION_STRING)  # type: ignore
    table_name = "iris"  # Replace with your table name
    rdb.pretty_print(rdb.select(table_name, "sepal_width", "species").limit(10).where_clause_on_col("sepal_width", "<=", 3.4).execute())

if __name__ == "__main__":
    main()