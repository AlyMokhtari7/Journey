from dataclasses import dataclass

import pandas as pd


@dataclass
class DataSet:
    data: pd.DataFrame

@dataclass
class DataBundle:
    features: dict[str, pd.DataFrame]
    target: dict[str, pd.DataFrame]
