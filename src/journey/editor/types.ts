export type nodeType = {
    id: string,
    position: { x: number, y: number },
    type?: string,
    data: { label: string, category: nodeCategory},
    // update_node: (data: {label: string, category: nodeCategory}) => void
}

export type edgeType = {
    id: string,
    source: string,
    target: string,
    // type: "smoothstep" | "step",
    type: string,
    label: string
}

export type DataSetProfile = {
  row_count: number,
  column_count: number,
  columns: Array<{
    name: string,
    dtype: string,
    distinct: number,
    missing: number,
    missing_percent: number,
    non_missing: number,
    most_frequent_value: string,
    numeric_summary: {
        min: number,
        max: number,
        mean: number,
        median: number,
        std: number,
    } | null,
  }>,
}

export type nodeCategory = "DataLoader/data" |
  "DataLoader/show_data_info" |
  "DataLoader/aggregate_data" |
  "DataLoader/data/loadCSV" |
  "DataLoader/data/loadDB" |
  "DataLoader/data/SkLearn" |

  "SQL/DB/GetInstance" |
  "SQL/Table/Select" |
  "SQL/ExecuteQuery" |

  "SkLearn/Scale" |
  "SkLearn/Normalize" |
  "SkLearn/Encode" |
  "SkLearn/DropMissingValues" |
  "SkLearn/Impute" |

  "SkLearn/DataSplit"
