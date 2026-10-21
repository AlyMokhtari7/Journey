import os

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import journey.backend.intermediate_artifacts
from journey.backend.intermediate_artifacts import DataSetProfile
from journey.backend.RDB import RDB
from journey.backend.workflow import Workflow

# --- Env Data ---
load_dotenv()
CONNECTION_STRING = os.getenv("CONNECTION_STRING")

from typing import Any

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

workflow = Workflow()

@app.post("/workflows/")
def execute_workflow(workflow_model: journey.backend.intermediate_artifacts.WorkflowModel):

    workflow.create_graph(workflow_model.nodes, workflow_model.edges)

    return {"status": "received"}

@app.get('/workflows/get_exec_res/{node_id}')
def get_exec_res(node_id: str):
    exec_res, node_type = workflow.get_exec_res(node_id=node_id)
    print(exec_res)
    return {'status': 200, 'exec_res': exec_res, 'node_type': node_type}

@app.get("/SQL/get_all_tables_name")
def get_all_tables_name():
    tables = RDB.get_all_tables_name()

    return {"tables": tables}

@app.get("/SQL/get_table_column_names/{table_name}")
def get_table_column_names(table_name: str):
    column_names = RDB.get_column_names(table_name)

    return {"column_names": column_names}
