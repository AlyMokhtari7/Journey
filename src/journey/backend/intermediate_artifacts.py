from typing_extensions import TypedDict
from jinja2.utils import missing
import enum
from dataclasses import dataclass
from typing import Any, Literal

import pandas as pd
from pydantic import BaseModel


@dataclass
class DataSet:
    data: pd.DataFrame

@dataclass
class DataBundle:
    features: dict[str, pd.DataFrame]
    target: dict[str, pd.DataFrame]


@dataclass
class DataSetProfileNumericColumnSummary:
    min: float
    max: float
    mean: float
    median: float
    std: float

@dataclass
class DataSetProfileColumn:
    name: str
    dtype: str
    distinct: int
    missing: int
    missing_percent: float
    non_missing: int
    most_frequent_value: str
    numeric_summary: DataSetProfileNumericColumnSummary | None


@dataclass
class DataSetProfile:
    row_count: int
    column_count: int
    columns: dict[str, DataSetProfileColumn]

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
    SQL_EXECUTE_QUERY ="SQL/ExecuteQuery"

    SKLEARN_SCALE = "SkLearn/Scale"
    SKLEARN_NORMALIZE = "SkLearn/Normalize"
    SKLEARN_ENCODE = "SkLearn/Encode"
    SKLEARN_DROP_MISSING_VALUES = "SkLearn/DropMissingValues"
    SKLEARN_IMPUTE = "SkLearn/Impute"

    SKLEARN_DATASPLIT = "SkLearn/DataSplit"



class ScaleContext(TypedDict):
    data_bundle: DataBundle
    method: Literal["standard", "robust", "minmax"]
    scale_target: bool

class SplitDataContext(TypedDict):
    data_set: DataSet
    random_state: int
    target_column: str
    test_size: float
