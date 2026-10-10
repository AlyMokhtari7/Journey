import enum
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
    data: dict | None = None

class WorkflowEdge(BaseModel):
    source: str
    target: str

class WorkflowModel(BaseModel):
    nodes: list[WorkflowNode]
    edges: list[WorkflowEdge]

class NodeCategory(str, enum.Enum):
    DATALOADER_DATA = "DataLoader/data"
    DATALOADER_DATA_LOAD_CSV = "DataLoader/data/loadCSV"
    DATALOADER_DATA_LOAD_SKLEARN = "DataLoader/data/SkLearn"
    DATALOADER_SHOW_DATA_INFO = "DataLoader/show_data_info"
    DATALOADER_AGGREGATE_DATA = "DataLoader/aggregate_data"

    SQL_GET_DB_INSTANCE ="SQL/DB/GetInstance"
    SQL_SELECT_ON_TABLE ="SQL/Table/Select"
