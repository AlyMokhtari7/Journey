from dataclasses import dataclass

import pandas as pd
from pydantic import BaseModel


@dataclass
class DataSet:
    data: pd.DataFrame

@dataclass
class DataBundle:
    features: dict[str, pd.DataFrame]
    target: dict[str, pd.DataFrame]

class WorkflowNode(BaseModel):
    id: str
    type: str | None = None


class WorkflowEdge(BaseModel):
    source: str
    target: str

class WorkflowModel(BaseModel):
    nodes: list[WorkflowNode]
    edges: list[WorkflowEdge]