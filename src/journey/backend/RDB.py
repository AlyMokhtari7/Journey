import os

import sqlalchemy as sa
from dotenv import load_dotenv
from sqlalchemy import Sequence, inspect
from tabulate import tabulate

# --- Env Data ---
load_dotenv()
CONNECTION_STRING = os.getenv("CONNECTION_STRING")

class RDB:

    @staticmethod
    def get_instance(connection_string: str) -> sa.engine.Engine:
        engine: sa.engine.Engine = sa.create_engine(connection_string)
        return engine

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

    # def __init__(self, connection_string: str):
    #     self._engine: sa.Engine = sa.create_engine(connection_string)
    #     self._metadata: sa.MetaData = sa.MetaData()
    #     self._query: sa.Select | None = None

    # ---------- Tables ----------

    @staticmethod
    def get_table(engine: sa.engine.Engine, metadata: sa.MetaData, table_name: str) -> sa.Table:
        return sa.Table(
            table_name,
            metadata,
            autoload_with=engine
        )

    # ---------- Query construction ----------

    @staticmethod
    def select(table_name: str, *columns: str, engine: sa.engine.Engine, metadata: sa.MetaData) -> sa.Select:
        table = RDB.get_table(engine, metadata, table_name)

        if columns:
            selected_columns = [
                getattr(table.c, column)
                for column in columns
            ]
            query = sa.select(*selected_columns)
        else:
            query = sa.select(table)

        return query

    @staticmethod
    def where_clause_on_col(query: sa.Select, col_name: str, operator: str, value) -> sa.Select:
        if query is None:
            raise RuntimeError("No query has been created.")

        table = RDB._get_current_table(query)
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

        query = query.where(condition)

        return query

    @staticmethod
    def group_by(query: sa.Select, *columns: str) -> sa.Select:
        if query is None:
            raise RuntimeError("No query has been created.")

        table = RDB._get_current_table(query)

        query = query.group_by(
            *(getattr(table.c, column) for column in columns)
        )

        return query

    @staticmethod
    def having(query: sa.Select, condition) -> sa.Select:
        if query is None:
            raise RuntimeError("No query has been created.")

        query = query.having(condition)
        return query

    @staticmethod
    def order_by(query: sa.Select, column: str, descending: bool = False) -> sa.Select:
        if query is None:
            raise RuntimeError("No query has been created.")

        table = RDB._get_current_table(query)

        column_obj = getattr(table.c, column)

        if descending:
            column_obj = column_obj.desc()

        query = query.order_by(column_obj)

        return query

    @staticmethod
    def limit(query: sa.Select, limit: int) -> sa.Select:
        if query is None:
            raise RuntimeError("No query has been created.")

        query = query.limit(limit)

        return query

    @staticmethod
    def offset(query: sa.Select, offset: int) -> sa.Select:
        if query is None:
            raise RuntimeError("No query has been created.")

        query = query.offset(offset)

        return query

    # ---------- Execution ----------

    @staticmethod
    def execute(query: sa.Select, engine: sa.engine.Engine) -> Sequence[sa.engine.Row]:
        if query is None:
            raise RuntimeError("No query has been created.")

        with engine.connect() as conn:
            result = conn.execute(query)
            return result.fetchall()  # type: ignore todo: fix this type issue

    # ---------- Utilities ----------

    @staticmethod
    def pretty_print(res):
        print(tabulate(res, headers="keys", tablefmt="pretty"))

    @staticmethod
    def show_query(query: sa.Select):
        if query is None:
            raise RuntimeError("No query has been created.")

        print(query)

    @staticmethod
    def _get_current_table(query: sa.Select):
        if query is None:
            raise RuntimeError("No query has been created.")

        # Get the first FROM clause
        froms = query.get_final_froms()

        if not froms:
            raise RuntimeError("Query has no table.")

        return froms[0]

def main():
    rdb = RDB()  # type: ignore
    table_name = "iris"
    engine: sa.engine.Engine = sa.create_engine(str(CONNECTION_STRING))
    metadata: sa.MetaData = sa.MetaData()
    query = rdb.select(table_name, "sepal_width", "species", engine = engine, metadata = metadata)
    query = rdb.limit(query, 10)
    query = rdb.where_clause_on_col(query, "sepal_width", "<=", 3.4)
    rdb.pretty_print(rdb.execute(query, engine))  # type: ignore

if __name__ == "__main__":
    main()