from __future__ import annotations

import os
from typing import Literal

import pandas as pd
from dotenv import load_dotenv
from sklearn.model_selection import train_test_split
from sqlalchemy import create_engine

from journey.intermediate_artifacts import DataSet

# --- Env Data ---
load_dotenv()
CSV_FILE_LOCATION = os.getenv("CSV_FILE_LOCATION")
SECOND_CSV_FILE_LOCATION = os.getenv("SECOND_CSV_FILE_LOCATION")


# --- Read DataSources ---
class DataLoader:
    def __init__(self, csv_file_location: str | None = CSV_FILE_LOCATION):
        __empty_df = pd.DataFrame()

        self._data_set: DataSet = DataSet(__empty_df)  # Initialize with an empty DataFrame
        

    def load_sklearn_sample_dateset(self) -> DataLoader:
        # for now it works with wine DataSet
        from sklearn.datasets import load_wine
        
        df = load_wine(return_X_y=False, as_frame=True)
        self._data_set = DataSet(df.frame) # type: ignore
        
        return self



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
            self._data_set.data = df
            return self
        except Exception as e:
            print(f"Error reading CSV file: {e}")
            self._data_set.data = pd.DataFrame()  # Set an empty DataFrame on error
            return self

    def read_from_postgres_to_pandas_df(
        self, connection_string: str, query: str
    ) -> DataLoader:
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
                self._data_set.data = df
                return self
        except Exception as e:
            print(f"Error reading from PostgreSQL: {e}")
            self._data_set.data = pd.DataFrame()  # Set an empty DataFrame on error
            return self

    def add_data_sources(
        self, df: pd.DataFrame, axis: Literal[0, 1] = 0, target_column: str = ""
    ) -> DataLoader:
        """
        Adds a DataFrame to the existing data.

        Args:
            df (pd.DataFrame): The DataFrame to add.
            axis (int): The axis along which to concatenate the DataFrames.

        Returns:
            DataLoader: The DataLoader instance with the added data.
        """
        if self._data_set.data.empty:
            self._data_set.data = df
        else:
            self._data_set.data = pd.concat([self._data_set.data, df], axis=axis)
            if target_column == "":
                target_column = str(
                    df.iloc[:, -1].name
                )  # Use the last column as the target if not specified
        return self

    def show_dataframe_info(self, df: pd.DataFrame | None = None) -> DataLoader:
        """
        Displays information about the DataFrame.

        Args:
            df (pd.DataFrame): The DataFrame to display information for.
        """
        if df is None:
            df = self._data_set.data
        print("-" * 10 + "DataFrame Info" + "-" * 10)
        df.info()
        print("-" * 10 + "DataFrame Head" + "-" * 10)
        print(df.head())
        return self


def main():
    data = DataLoader()
    # data.add_data_sources(
    #     pd.read_csv(str(CSV_FILE_LOCATION))
    # ).show_dataframe_info().add_data_sources(
    #     pd.read_csv(str(SECOND_CSV_FILE_LOCATION)), axis=1
    # ).show_dataframe_info()

    data.load_sklearn_sample_dateset()


if __name__ == "__main__":
    main()
