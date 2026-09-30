from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class WorkflowNode(BaseModel):
    id: str
    type: str | None = None


class WorkflowEdge(BaseModel):
    source: str
    target: str

class Workflow(BaseModel):
    nodes: list[WorkflowNode]
    edges: list[WorkflowEdge]


@app.post("/workflows/")
def execute_workflow(workflow: Workflow):
    print('------Workflow nodes-------\n', workflow.nodes)
    print('------Workflow edges-------\n', workflow.edges)

    return {"status": "received"}