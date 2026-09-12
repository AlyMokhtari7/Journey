import pandas as pd

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

def main() -> None:
    print("Hello from journey!")
    df = read_csv("titanic.csv")
    show_dataframe_info(df)

if __name__ == "__main__":
    main()