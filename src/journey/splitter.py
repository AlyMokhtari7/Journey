import pandas as pd
from sklearn.model_selection import train_test_split

from journey.intermediate_artifacts import DataBundle, DataSet


class Splitter:
    def __init__(self) -> None:
        self._data_bundle: DataBundle

    @staticmethod
    def split_data(
        dataset: DataSet,
        target_column: str = "",
        test_size: float = 0.2,
        random_state: int = 42,
    ):
        """
        Splits the DataFrame into training and testing sets.

        Args:
            df (pd.DataFrame): The DataFrame to split.
            target_column (str): The name of the target column.
            test_size (float): The proportion of the dataset to include in the test split.
            random_state (int): Random seed for reproducibility.

        Returns:
            tuple: A tuple containing the training and testing sets (X_train, X_test, y_train, y_test).
        """
        df = dataset.data

        if target_column == "":
            target_column = str(
                df.iloc[:, -1].name
            )  # Use the last column as the target if not specified

        X = df.drop(columns=[target_column])
        y = df[target_column]

        _X_train, _X_test, _y_train, _y_test = train_test_split(X, y, test_size=test_size, random_state=random_state)

        return DataBundle({"_X_train": _X_train, "_X_test": _X_test}, {"_y_train": _y_train, "_y_test": _y_test})
    