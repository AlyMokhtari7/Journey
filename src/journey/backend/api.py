from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import journey.backend.intermediate_artifacts
from journey.backend.workflow import Workflow

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/workflows/")
def execute_workflow(workflow_model: journey.backend.intermediate_artifacts.WorkflowModel):
    workflow = Workflow()

    workflow.create_graph(workflow_model.nodes, workflow_model.edges)

    return {"status": "received"}