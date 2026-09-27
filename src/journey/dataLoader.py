from __future__ import annotations
import pandas as pd
from dotenv import load_dotenv
import os
from sklearn.impute import SimpleImputer
from sqlalchemy import create_engine


# --- Env Data ---
load_dotenv()
CSV_FILE_LOCATION = os.getenv("CSV_FILE_LOCATION")

# --- Read DataSources ---
class DataLoader:
    def __init__(self, csv_file_location: str | None = CSV_FILE_LOCATION):
        self.csv_file_location = csv_file_location
        self._data: pd.DataFrame = pd.DataFrame()  # Initialize with an empty DataFrame

    def read_csv(self, file_path: str) -> DataLoader:
        """
        Reads a CSV file and returns a pandas DataFrame.

        Args:
            file_path (str): The path to the CSV file.
        
        Returns:
            DataLoader: The DataLoader instance with the loaded data.
        """
        try:
            df = pd.read_csv(file_path)
            self._data = df
            return self
        except Exception as e:
            print(f"Error reading CSV file: {e}")
            self._data = pd.DataFrame()  # Set an empty DataFrame on error
            return self

    def read_from_postgres_to_pandas_df(self, connection_string: str, query: str) -> DataLoader:
        """
        Reads data from a PostgreSQL database and returns a pandas DataFrame.

        Args:
            connection_string (str): The connection string for the PostgreSQL database.
            query (str): The SQL query to execute.
        
        Returns:
            DataLoader: The DataLoader instance with the loaded data.
        """
        try:
            with create_engine(connection_string).connect() as conn:
                df = pd.read_sql_query(query, conn)
                self._data = df
                return self
        except Exception as e:
            print(f"Error reading from PostgreSQL: {e}")
            self._data = pd.DataFrame()  # Set an empty DataFrame on error
            return self

    def __aggregate_data_sources(self, dfs: list[pd.DataFrame]) -> DataLoader:
        """
        Aggregates multiple DataFrames into a single DataFrame.

        Args:
            dfs (list[pd.DataFrame]): A list of DataFrames to aggregate.

        Returns:
            DataLoader: The DataLoader instance with the aggregated data.
        """
        self._data = pd.concat(dfs, ignore_index=True)
        return self

    def show_dataframe_info(self, df: pd.DataFrame) -> DataLoader:
        """
        Displays information about the DataFrame.

        Args:
            df (pd.DataFrame): The DataFrame to display information for.
        """
        print("DataFrame Info:")
        print(self._data.info())
        print("\nDataFrame Head:")
        print(self._data.head())
        return self

def main():
    data = DataLoader()
    data.read_csv(str(CSV_FILE_LOCATION)).show_dataframe_info(data._data)

if __name__ == "__main__":
    main()