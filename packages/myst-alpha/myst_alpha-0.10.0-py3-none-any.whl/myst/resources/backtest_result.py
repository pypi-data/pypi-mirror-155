import json
import warnings
from typing import Any, Dict, Mapping, Optional

import httpx
import pandas as pd

from myst.client import get_client
from myst.core.time.time import Time
from myst.models.time_dataset import TimeDataset
from myst.models.types import UUIDOrStr, to_uuid
from myst.openapi.api.projects.backtests.results import get_backtest_result
from myst.resources.resource import Resource


def _download_result(result_url: str) -> Dict[str, Any]:
    """Downloads the backtest result from the supplied URL and parses it."""
    response = httpx.get(result_url)

    if response.status_code == 200:
        result_data = json.loads(response.content)
    else:
        raise RuntimeError("Could not download backtest result.")

    return result_data


class BacktestResult(Resource):

    start_time: Time
    end_time: Time
    result_url: str
    metrics: Optional[Mapping[str, Optional[float]]]

    @classmethod
    def get(self, project_uuid: UUIDOrStr, backtest_uuid: UUIDOrStr, job_uuid: UUIDOrStr) -> "BacktestResult":
        backtest_result = get_backtest_result.request_sync(
            client=get_client(),
            project_uuid=str(to_uuid(project_uuid)),
            backtest_uuid=str(to_uuid(backtest_uuid)),
            job_uuid=str(to_uuid(job_uuid)),
        )

        return BacktestResult.parse_obj(backtest_result.dict())

    def to_pandas_data_frame(self) -> pd.DataFrame:
        """Downloads the backtest result and converts the time arrays to pandas data frames.

        Data will be re-indexed against the predictions' natural time index, dropping any target data that doesn't
        correspond to a prediction.

        Returns:
            a pandas data frame with the predictions made by the backtest, and their corresponding targets

        Raises:
            NotImplementedError: for result data with more than one target
        """
        result_data = _download_result(result_url=self.result_url)

        # Assume that there is only one target for now.
        if len(result_data["targets"]) != 1:
            raise NotImplementedError

        # Aggregate all predictions into a list of data frames, setting the index to both `time` and `reference_time`.
        prediction_pandas_objects = []
        for fold in result_data["fold_results"]:
            for predict_result in fold["predict_results"]:
                for prediction in predict_result["predictions"]:
                    prediction_time_dataset = TimeDataset.parse_obj(prediction)
                    # Disable an argument deprecated warning.
                    with warnings.catch_warnings():
                        warnings.filterwarnings(
                            "ignore",
                            category=FutureWarning,
                            message="Argument `closed` is deprecated in favor of `inclusive`.",
                        )
                        prediction_pandas_object = prediction_time_dataset.flatten().to_pandas_object()

                    multi_index = pd.MultiIndex.from_product(
                        [prediction_pandas_object.index, [pd.Timestamp(predict_result["reference_time"])]],
                        names=["time", "reference_time"],
                    )
                    prediction_pandas_objects.append(prediction_pandas_object.set_axis(multi_index, inplace=False))

        # Create the prediction data frame.
        prediction_pandas_object = pd.concat(prediction_pandas_objects)

        # Create the target data frame.
        with warnings.catch_warnings():
            warnings.filterwarnings(
                "ignore", category=FutureWarning, message="Argument `closed` is deprecated in favor of `inclusive`."
            )
            target_pandas_object = TimeDataset.parse_obj(result_data["targets"][0]).flatten().to_pandas_object()

        # Re-index the target data frame against the `time` index of the predictions, ensuring that we can make a
        # combined data frame with a single natural time index.
        target_pandas_object = target_pandas_object.reindex(
            prediction_pandas_object.index.get_level_values("time")
        ).set_axis(prediction_pandas_object.index, inplace=False)

        # Return the combined data frame.
        pandas_data_frame = pd.concat(
            [target_pandas_object, prediction_pandas_object], axis=1, keys=["targets", "predictions"]
        )

        return pandas_data_frame
