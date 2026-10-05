from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import journey.backend.intermediate_artifacts
from journey.backend.workflow import Workflow
from journey.backend.RDB import RDB

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

    print('Asked me hehye -- api')

    return {"tables": tables}

@app.get("/SQL/get_table_column_names/{table_name}")
def get_table_column_names(table_name: str):
    column_names = RDB.get_column_names(table_name)
    print('Asked me -- api')

    return {"column_names": column_names}

@app.get("/SQL/execute_query/{table_name}/{columns}")
def execute_query(table_name: str, columns: str, limit: int = 10):
    column_list = columns.split(",")
    workflow._dbRes = workflow._dbManager.select(table_name, *column_list).limit(limit).execute() # type: ignore
    workflow._dbManager.pretty_print(workflow._dbRes)

    print('Query executed')
    return {"status": "query executed"}