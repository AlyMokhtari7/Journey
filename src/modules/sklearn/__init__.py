from typing import Any, Literal, TypedDict

import pandas as pd
from fontTools.misc.plistlib import Data
from pygments.unistring import Sc

from journey.backend.intermediate_artifacts import DataBundle, DataSet
from journey.sdk.base import NodeModel
from sklearn import preprocessing
from sklearn.model_selection import train_test_split

type AnyScaler = preprocessing.StandardScaler | preprocessing.RobustScaler | preprocessing.MinMaxScaler

class BaseResult(TypedDict):
    res: DataSet | DataBundle


class ScaleResult(BaseResult):
    scaler: AnyScaler
    target_scaler: AnyScaler | None

class EncodeResult(BaseResult):
    encoder: preprocessing.OrdinalEncoder


class Preprocessing:

    class ScaleData(NodeModel):

        def _scale_dataBundle(self, data_bundle: DataBundle,
            method: str = "standard", scale_target: bool = False
        ) -> ScaleResult:
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

            X_train = data_bundle.features["_X_train"]
            Scalers["features"].fit(X_train)  # Fit the scaler on the training data

            if scale_target:
                Scalers["target"] = Scaler_methods[method]()
                Scalers["target"].fit(data_bundle.target["_y_train"])

            for split, scaler in Scalers.items():
                data_bundle_part = getattr(data_bundle, split)
                for subset, data in data_bundle_part.items():
                    subset_scaled = scaler.transform(data)

                    # Preserve DataFrame structure if the inputs are DataFrames
                    data_bundle_part[subset] = pd.DataFrame(
                        subset_scaled,
                        columns=data.columns,
                        index=data.index,
                    )

            _scaler = Scalers["features"]
            _target_scaler = None
            if scale_target:
                _target_scaler = Scalers["target"]

            return ScaleResult(res=data_bundle, scaler=_scaler, target_scaler=_target_scaler if scale_target else None)


        def _scale_dataSet(self, data_set: DataSet,
            method: str = "standard", scale_target: bool = False
        ) -> ScaleResult:
            """
            Scales a DataSet using the specified method and returns a ScaleResult.
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

            data = data_set.data
            _scaler = Scalers["features"]
            _target_scaler = None

            data_columns = data.columns
            data_index = data.index
            data = _scaler.fit_transform(data)

            data = pd.DataFrame(
                data,
                columns=data_columns,
                index=data_index,
            )

            return ScaleResult(res=DataSet(data=data), scaler=_scaler, target_scaler=None)


        def execute(self, context: dict[str, Any], utils) -> ScaleResult:
            data: DataBundle | DataSet = context['data_bundle']
            method: Literal["standard", "robust", "minmax"] = context['method']
            scale_target: bool = context['scale_target']
            if isinstance(data, DataSet):
                exec_res: ScaleResult = self._scale_dataSet(data_set=data, method=method, scale_target=scale_target)
            elif isinstance(data, DataBundle):
                exec_res: ScaleResult = self._scale_dataBundle(data_bundle=data, method=method, scale_target=scale_target)
            utils.log(log_msg='Finished_Scaling_Data', node_name='SkLearn')
            return exec_res

    class NormalizeData(NodeModel):

        def _normalize_vectors(
            self, databundle: DataBundle, norm: Literal["l1", "l2", "max"] = "l1", normalize_target: bool = False
        ) -> DataBundle:

            splits_to_normalize = ["features"]

            if normalize_target:
                splits_to_normalize.append("target")

            for split in splits_to_normalize:
                data_bundle_part = getattr(databundle, split)
                for subset, data in data_bundle_part.items():
                    subset_normalized = preprocessing.normalize(data, norm=norm)

                    # Preserve DataFrame structure if the inputs are DataFrames
                    data_bundle_part[subset] = pd.DataFrame(
                        subset_normalized,
                        columns=data.columns,
                        index=data.index,
                    )

            return databundle


        def execute(self, context: dict[str, Any], utils) -> BaseResult:
            data_bundle = context['data_bundle']
            norm = context['norm']
            normalize_target = context['normalize_target']
            exec_res = self._normalize_vectors(databundle=data_bundle, norm=norm, normalize_target=normalize_target)
            utils.log(log_msg='Finished_Normalizing_Data', node_name='SkLearn')
            return BaseResult(res=exec_res)

    class EncodeDataFeatures(NodeModel):

        def _encode_data_features(self, databundle: DataBundle) -> EncodeResult:
            enc = preprocessing.OrdinalEncoder(
                handle_unknown="use_encoded_value",
                unknown_value=-1,
            )

            data_bundle_part = databundle.features

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

            _encoder = enc

            return EncodeResult(res=databundle, encoder=_encoder)


        def execute(self, context: dict[str, Any], utils) -> EncodeResult:
            data_bundle = context['data_bundle']
            exec_res = self._encode_data_features(databundle=data_bundle)
            utils.log(log_msg='Finished_Encoding_Data_Features', node_name='SkLearn')
            return exec_res

    class DropMissingValues(NodeModel):

        def _drop_columns_with_missing_values_from_dataset(self, data: DataSet) -> BaseResult:
            """
            Drops columns from the DataFrame that contain any missing values.

            Args:
                data (DataSet): The DataSet to process.

            Returns:
                BaseResult: A DataSet with columns containing missing values dropped.
            """
            return BaseResult(res=DataSet(data.data.dropna(axis=0)))


        def _drop_columns_with_missing_values_from_databundle(self, data: DataBundle) -> BaseResult:
            return BaseResult(
                res=DataBundle(
                    features={
                        "_X_train": data.features["_X_train"].dropna(axis=0),
                        "_X_test": data.features["_X_test"].dropna(axis=0),
                    },
                    target={
                        "_y_train": data.target["_y_train"].dropna(),
                        "_y_test": data.target["_y_test"].dropna(),
                    },
                )
            )

        def execute(self, context: dict[str, Any], utils) -> BaseResult:
            data_frame = context['data_frame']
            if isinstance(data_frame, DataBundle):
                exec_res = self._drop_columns_with_missing_values_from_databundle(data_frame)
            else:
                exec_res = self._drop_columns_with_missing_values_from_dataset(data_frame)
            utils.log(log_msg='Finished_Dropping_Missing_Values', node_name='SkLearn')
            return exec_res

    class ImputeData(NodeModel):

        def _imputation(self, df: pd.DataFrame, strategy: str = "mean") -> BaseResult:
            """
            Imputes missing values in the DataFrame using the specified strategy.

            Args:
                df (pd.DataFrame): The DataFrame to process.
                strategy (str): The imputation strategy ('mean', 'median', or 'mode').

            Returns:
                BaseResult: A DataSet with missing values imputed.
            """
            if strategy == "mean":
                return BaseResult(res=DataSet(df.fillna(df.mean())))
            elif strategy == "median":
                return BaseResult(res=DataSet(df.fillna(df.median())))
            elif strategy == "mode":
                return BaseResult(res=DataSet(df.fillna(df.mode().iloc[0])))
            else:
                raise ValueError(
                    "Invalid imputation strategy. Choose 'mean', 'median', or 'mode'."
                )


        def execute(self, context: dict[str, Any], utils) -> BaseResult:
            data_frame = context['data_frame']
            exec_res = self._imputation(df=data_frame)
            utils.log(log_msg='Finished_Encoding_Data_Features', node_name='SkLearn')
            return exec_res

class DataSplitter(NodeModel):

    def _split_data(
        self,
        dataset: DataSet,
        target_column: str = "",
        test_size: float = 0.2,
        random_state: int = 42,
    ) -> BaseResult:
        """
        Splits the DataSet into training and testing sets.

        Args:
            dataset (DataSet): The DataSet to split.
            target_column (str): The name of the target column.
            test_size (float): The proportion of the dataset to include in the test split.
            random_state (int): Random seed for reproducibility.

        Returns:
            BaseResult: A DataBundle containing the training and testing sets (X_train, X_test, y_train, y_test).
        """
        df = dataset.data

        if target_column == "":
            target_column = str(
                df.iloc[:, -1].name
            )  # Use the last column as the target if not specified

        X = df.drop(columns=[target_column])
        y = df[target_column]

        _X_train: Any
        _X_test: Any
        _y_train: Any
        _y_test: Any

        _X_train, _X_test, _y_train, _y_test = train_test_split(X, y, test_size=test_size, random_state=random_state)

        return BaseResult(res=DataBundle({"_X_train": _X_train, "_X_test": _X_test}, {"_y_train": _y_train, "_y_test": _y_test}))

    def execute(self, context: dict[str, Any], utils) -> BaseResult:
        data_set = context['data_set']
        random_state = context['random_state']
        target_column = context['target_column']
        test_size = context['test_size']
        exec_res = self._split_data(dataset=data_set, random_state=random_state, target_column=target_column, test_size=test_size)
        utils.log(log_msg='Finished_Splitting_Data_Features', node_name='SkLearn')
        return exec_res

class SklearnDataSets(NodeModel):

    def _load_sklearn_sample_dateset(self) -> BaseResult:
        # for now it works with wine DataSet
        from sklearn.datasets import load_wine

        df = load_wine(return_X_y=False, as_frame=True)
        return BaseResult(res=DataSet(df.frame))

    def execute(self, context: dict[str, Any], utils) -> BaseResult:
        exec_res = self._load_sklearn_sample_dateset()
        utils.log(log_msg='Finished_Loading_Data_Features', node_name='SkLearn')
        return exec_res
