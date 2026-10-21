import type { DataSetProfile } from "../types";

export default function DatasetProfile({ profile }: { profile: DataSetProfile }) {
  const column_numeric_summary_cell = (summary: { min: number; max: number; mean: number; median: number; std: number } | null) => {
    if (!summary) return null;
    return (
      <div>
        <p>Min: {summary.min}</p>
        <p>Max: {summary.max}</p>
        <p>Mean: {summary.mean}</p>
        <p>Median: {summary.median}</p>
        <p>Std: {summary.std}</p>
      </div>
    );
  };

  const columns_data_table = profile.columns.map((column) => (
    <tr key={column.name}>
      <td>{column.name}</td>
      <td>{column.dtype}</td>
      <td>{column.distinct}</td>
      <td>{column.missing}</td>
      <td>{column.missing_percent}</td>
      <td>{column.non_missing}</td>
      <td>{column.most_frequent_value}</td>
      <td>{column_numeric_summary_cell(column.numeric_summary)}</td>
    </tr>
  ));

  return (
    <div>
      <h3>{profile.row_count}</h3>
      <p>{profile.column_count}</p>
      <hr />
      <table>
        <thead>
          <tr>
            <th>Name</th>
            <th>Dtype</th>
            <th>Distinct</th>
            <th>Missing</th>
            <th>Missing Percentage</th>
            <th>Non Missing</th>
            <th>Most Frequent Value</th>
            <th>Numeric Summary</th>
          </tr>
        </thead>
        <tbody>
          {columns_data_table}
        </tbody>
      </table>
    </div>
  );
}
