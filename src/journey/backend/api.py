import os

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import journey.backend.intermediate_artifacts
from journey.backend.RDB import RDB
from journey.backend.workflow import Workflow

# --- Env Data ---
load_dotenv()
CONNECTION_STRING = os.getenv("CONNECTION_STRING")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

workflow = Workflow()

@app.post("/workflows/")
def execute_workflow(workflow_model: journey.backend.intermediate_artifacts.WorkflowModel):
    
    workflow.create_graph(workflow_model.nodes, workflow_model.edges)

    return {"status": "received"}

@app.get("/SQL/get_all_tables_name")
def get_all_tables_name():
    tables = RDB.get_all_tables_name()

    return {"tables": tables}

@app.get("/SQL/get_table_column_names/{table_name}")
def get_table_column_names(table_name: str):
    column_names = RDB.get_column_names(table_name)

    return {"column_names": column_names}

# @app.get("/SQL/execute_query/{table_name}/{columns}")
# def execute_query(table_name: str, columns: str, limit: int = 10):
#     engine = RDB.get_instance(str(CONNECTION_STRING))
#     metadata = sa.MetaData()

#     column_list = columns.split(",")
#     _dbRes = RDB.select(table_name, *column_list, engine=engine, metadata=metadata)
#     _dbRes = RDB.limit(_dbRes, limit)
#     _dbRes = RDB.execute(engine=engine, query=_dbRes)
#     RDB.pretty_print(_dbRes)

#     print('Query executed')
#     return {"status": "query executed"}