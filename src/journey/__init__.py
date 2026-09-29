import pandas as pd
from dotenv import load_dotenv
import os
from sklearn.impute import SimpleImputer
from sqlalchemy import create_engine

load_dotenv()
CSV_FILE_LOCATION = os.getenv("CSV_FILE_LOCATION")


def main() -> None:
    print("Hello from journey!")
    

if __name__ == "__main__":
    main()