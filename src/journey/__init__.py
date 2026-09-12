import pandas as pd
from dotenv import load_dotenv
import os
from sqlalchemy import create_engine

load_dotenv()
CSV_FILE_LOCATION = os.getenv("CSV_FILE_LOCATION")

def read_csv(file_path: str) -> pd.DataFrame:
    """
    Reads a CSV file and returns a pandas DataFrame.

    Args:
        file_path (str): The path to the CSV file.
    
    Returns:
        pd.DataFrame: A DataFrame containing the data from the CSV file.
    """
    try:
        df = pd.read_csv(file_path)
        return df
    except Exception as e:
        print(f"Error reading CSV file: {e}")
        return pd.DataFrame()  # Return an empty DataFrame on error

def show_dataframe_info(df: pd.DataFrame) -> None:
    """
    Displays information about the DataFrame.

    Args:
        df (pd.DataFrame): The DataFrame to display information for.
    """
    print("DataFrame Info:")
    print(df.info())
    print("\nDataFrame Head:")
    print(df.head())

def read_from_postgres_to_pandas_df(connection_string: str, query: str) -> pd.DataFrame:
    """
    Reads data from a PostgreSQL database and returns a pandas DataFrame.

    Args:
        connection_string (str): The connection string for the PostgreSQL database.
        query (str): The SQL query to execute.
    
    Returns:
        pd.DataFrame: A DataFrame containing the data retrieved from the database.
    """
    try:
        with create_engine(connection_string).connect() as conn:
            df = pd.read_sql_query(query, conn)
            return df
    except Exception as e:
        print(f"Error reading from PostgreSQL: {e}")
        return pd.DataFrame()  # Return an empty DataFrame on error

def main() -> None:
    print("Hello from journey!")
    # df = read_csv(f"{CSV_FILE_LOCATION}")
    # show_dataframe_info(df)
    db_df = read_from_postgres_to_pandas_df("postgresql://postgres:1936@localhost:5432", "SELECT * FROM public.iris")
    show_dataframe_info(db_df)

if __name__ == "__main__":
    main()