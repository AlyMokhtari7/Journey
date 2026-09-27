import pandas as pd
from dotenv import load_dotenv
import os
from sklearn.impute import SimpleImputer
from sqlalchemy import create_engine

load_dotenv()
CSV_FILE_LOCATION = os.getenv("CSV_FILE_LOCATION")


def drop_columns_with_missing_values(df: pd.DataFrame) -> pd.DataFrame:
    """
    Drops columns from the DataFrame that contain any missing values.

    Args:
        df (pd.DataFrame): The DataFrame to process.

    Returns:
        pd.DataFrame: A DataFrame with columns containing missing values dropped.
    """
    return df.dropna(axis=1)

def imputation(df: pd.DataFrame, strategy: str = "mean") -> pd.DataFrame:
    """
    Imputes missing values in the DataFrame using the specified strategy.

    Args:
        df (pd.DataFrame): The DataFrame to process.
        strategy (str): The imputation strategy ('mean', 'median', or 'mode').

    Returns:
        pd.DataFrame: A DataFrame with missing values imputed.
    """
    if strategy == "mean":
        return df.fillna(df.mean())
    elif strategy == "median":
        return df.fillna(df.median())
    elif strategy == "mode":
        return df.fillna(df.mode().iloc[0])
    else:
        raise ValueError("Invalid imputation strategy. Choose 'mean', 'median', or 'mode'.")

def imputation_with_exteention(df: pd.DataFrame) -> pd.DataFrame:
    """
    Imputes missing values in the DataFrame and adds indicator columns for missing values.
    
    Returns:
        pd.DataFrame: A DataFrame with missing values imputed and indicator columns added.
    """

    # Get names of columns with missing values
    cols_with_missing = [col for col in df.columns if df[col].isnull().any()]

    temp_df = df.copy()
    
    for col in cols_with_missing:
        temp_df[col + '_was_missing'] = temp_df[col].isnull()

    my_imputer = SimpleImputer()
    imputed_df = pd.DataFrame(my_imputer.fit_transform(temp_df))

    # Imputation removed column names; put them back
    imputed_df.columns = temp_df.columns
    return imputed_df

def main() -> None:
    print("Hello from journey!")
    # df = read_csv(f"{CSV_FILE_LOCATION}")
    # show_dataframe_info(df)
    # db_df = read_from_postgres_to_pandas_df("postgresql://postgres:1936@localhost:5432", "SELECT * FROM public.iris")
    # show_dataframe_info(db_df)
    

if __name__ == "__main__":
    main()