from __future__ import annotations

from typing import Literal

import pandas as pd
from sklearn import preprocessing
from sklearn.impute import SimpleImputer

from journey.backend.intermediate_artifacts import DataBundle, DataSet
from journey.backend.splitter import Splitter


class DataProcessor:
    def __init__(self, dataset: DataSet):
        self._data_bundle: DataBundle = Splitter.split_data(dataset)
        self._processing_steps: list[str] = []
        self._scaler: preprocessing.StandardScaler | preprocessing.RobustScaler | preprocessing.MinMaxScaler = preprocessing.StandardScaler()
        self._target_scaler = None
        self._encoders = {}

    def process_data(self, df: pd.DataFrame):
        pass

    # --------- Scaling -----------
    def scale_data(
        self, method: str = "standard", scale_target: bool = False
    ) -> DataProcessor:
        """
        Scales the data in the DataFrame using the specified scaling method.

        Args:
            df (pd.DataFrame): The DataFrame to scale.
            method (str): The scaling method ('standard', 'minmax', or 'robust').

        Returns:
            pd.DataFrame: A DataFrame with scaled data.
        """

        Scaler_methods = {
            "standard": preprocessing.StandardScaler,
            "minmax": preprocessing.MinMaxScaler,
            "robust": preprocessing.RobustScaler,
        }

        if method not in Scaler_methods:
            raise ValueError(
                "Invalid scaling method. Choose 'standard', 'minmax', or 'robust'."
            )

        # Holds all the scalers, including the target scaler if needed
        Scalers = {"features": Scaler_methods[method]()}

        X_train = self._data_bundle.features["_X_train"]
        Scalers["features"].fit(X_train)  # Fit the scaler on the training data

        if scale_target:
            Scalers["target"] = Scaler_methods[method]()
            Scalers["target"].fit(self._data_bundle.target["_y_train"])

        for split, scaler in Scalers.items():
            data_bundle_part = getattr(self._data_bundle, split)
            for subset, data in data_bundle_part.items():
                subset_scaled = scaler.transform(data)

                # Preserve DataFrame structure if the inputs are DataFrames
                data_bundle_part[subset] = pd.DataFrame(
                    subset_scaled,
                    columns=data.columns,
                    index=data.index,
                )

        self._scaler = Scalers["features"]
        if scale_target:
            self._target_scaler = Scalers["target"]

        return self

    # --------- Normalization -----------
    def normalize_vectors(
        self, norm: Literal["l1", "l2", "max"] = "l1", normalize_target: bool = False
    ) -> DataProcessor:

        splits_to_normalize = ["features"]

        if normalize_target:
            splits_to_normalize.append("target")

        for split in splits_to_normalize:
            data_bundle_part = getattr(self._data_bundle, split)
            for subset, data in data_bundle_part.items():
                subset_normalized = preprocessing.normalize(data, norm=norm)

                # Preserve DataFrame structure if the inputs are DataFrames
                data_bundle_part[subset] = pd.DataFrame(
                    subset_normalized,
                    columns=data.columns,
                    index=data.index,
                )

        return self

    # --------- Encoding -----------
    def encode_data_features(self) -> DataProcessor:
        enc = preprocessing.OrdinalEncoder(
            handle_unknown="use_encoded_value",
            unknown_value=-1,
        )

        data_bundle_part = self._data_bundle.features

        categorical_cols = (
            data_bundle_part["_X_train"]
            .select_dtypes(include=["object", "category"])
            .columns.tolist()
        )  # Cat-cols from _X_train is the same as _X_test

        enc.fit(data_bundle_part["_X_train"][categorical_cols])

        for subset, data in data_bundle_part.items():
            encoded_subset = enc.transform(data[categorical_cols])

            data = data.copy()

            data.loc[:, categorical_cols] = encoded_subset

            data_bundle_part[subset] = data

        self._encoders["ordinal"] = enc

        return self

    def drop_columns_with_missing_values(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Drops columns from the DataFrame that contain any missing values.

        Args:
            df (pd.DataFrame): The DataFrame to process.

        Returns:
            pd.DataFrame: A DataFrame with columns containing missing values dropped.
        """
        return df.dropna(axis=1)

    def imputation(self, df: pd.DataFrame, strategy: str = "mean") -> pd.DataFrame:
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
            raise ValueError(
                "Invalid imputation strategy. Choose 'mean', 'median', or 'mode'."
            )

    def imputation_with_extention(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Imputes missing values in the DataFrame and adds indicator columns for missing values.

        Returns:
            pd.DataFrame: A DataFrame with missing values imputed and indicator columns added.
        """

        # Get names of columns with missing values
        cols_with_missing = [col for col in df.columns if df[col].isnull().any()]

        temp_df = df.copy()

        for col in cols_with_missing:
            temp_df[col + "_was_missing"] = temp_df[col].isnull()

        my_imputer = SimpleImputer()
        imputed_df = pd.DataFrame(my_imputer.fit_transform(temp_df))

        # Imputation removed column names; put them back
        imputed_df.columns = temp_df.columns
        return imputed_df
