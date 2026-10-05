from __future__ import annotations

import os
from typing import Literal

import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine

from journey.backend.intermediate_artifacts import DataSet

# --- Env Data ---
load_dotenv()
CSV_FILE_LOCATION = os.getenv("CSV_FILE_LOCATION")
SECOND_CSV_FILE_LOCATION = os.getenv("SECOND_CSV_FILE_LOCATION")


# --- Read DataSources ---
class DataLoader:
    # def __init__(self, csv_file_location: str | None = CSV_FILE_LOCATION):
    #     __empty_df = pd.DataFrame()

    #     self._data_set: DataSet = DataSet(__empty_df)  # Initialize with an empty DataFrame
        

    @staticmethod
    def load_sklearn_sample_dateset() -> DataSet:
        # for now it works with wine DataSet
        from sklearn.datasets import load_wine
        
        df = load_wine(return_X_y=False, as_frame=True)
        return DataSet(df.frame) # type: ignore


    @staticmethod
    def read_csv(file_path: str = str(CSV_FILE_LOCATION)) -> DataSet:
        """
        Reads a CSV file and returns a pandas DataFrame.

        Args:
            file_path (str): The path to the CSV file.

        Returns:
            DataSet: The DataSet instance with the loaded data.
        """
        try:
            df = pd.read_csv(file_path)
            return DataSet(df)
        except Exception as e:
            print(f"Error reading CSV file: {e}")
            return DataSet(pd.DataFrame()) # return an empty DataFrame on error

    @staticmethod
    def read_from_postgres_to_pandas_df(
        connection_string: str, query: str
    ) -> DataSet:
        """
        Reads data from a PostgreSQL database and returns a pandas DataFrame.

        Args:
            connection_string (str): The connection string for the PostgreSQL database.
            query (str): The SQL query to execute.

        Returns:
            DataSet: The DataSet instance with the loaded data.
        """
        try:
            with create_engine(connection_string).connect() as conn:
                df = pd.read_sql_query(query, conn)
                return DataSet(df)
        except Exception as e:
            print(f"Error reading from PostgreSQL: {e}")
            return DataSet(pd.DataFrame())  # return an empty DataFrame on error

    @staticmethod
    def add_data_sources(
        df: pd.DataFrame, axis: Literal[0, 1] = 1, target_column: str = ""
    ) -> DataSet:
        # Todo: Target column should be handled properly, for now it is just a placeholder
        
        """
        Adds a DataFrame to the existing data.

        Args:
            df (pd.DataFrame): The DataFrame to add.
            axis (int): The axis along which to concatenate the DataFrames.

        Returns:
            DataSet: The DataSet instance with the added data.
        """
        if df.empty:
            return DataSet(pd.DataFrame())
        else:
            return DataSet(pd.concat([df, df], axis=axis))

    @staticmethod
    def show_dataframe_info(df: pd.DataFrame) -> None:
        """
        Displays information about the DataFrame.

        Args:
            df (pd.DataFrame): The DataFrame to display information for.
        """
        print("-" * 10 + "DataFrame Info" + "-" * 10)
        df.info()
        print("-" * 10 + "DataFrame Head" + "-" * 10)
        print(df.head())

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
