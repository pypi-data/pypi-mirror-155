# -*- coding: utf-8 -*-
import os
import mlflow
import pandas as pd
from pathlib import Path
from mlflow.tracking.client import MlflowClient


def main(
        path_to_dataset: str,
        path_to_predictions_storage: str,
        registered_model_name,
        dagshub_mlflow_tracking_uri: str,
        mlflow_tracking_username: str,
        mlflow_tracking_password: str,

) -> None:
    """
    Runs model's predict method
    Args:
        path_to_dataset: absolute path to your dataset
        path_to_predictions_storage: absolute path to your predictions storage
        registered_model_name: the name of th model in mlflow model's registry
        dagshub_mlflow_tracking_uri: path to mlflow uri provided by dags hub
        mlflow_tracking_username: dags hub username
        mlflow_tracking_password: dags hub token
    Returns:
        object: None
    """
    os.environ["MLFLOW_TRACKING_USERNAME"] = mlflow_tracking_username
    os.environ["MLFLOW_TRACKING_PASSWORD"] = mlflow_tracking_password

    mlflow.set_tracking_uri(dagshub_mlflow_tracking_uri)

    client = MlflowClient()

    path_to_dataset = Path(path_to_dataset)
    path_to_predictions_storage = Path(path_to_predictions_storage)

    # read dataset
    x_test = pd.read_csv(path_to_dataset)

    # Now separate the dataset as response variable and feature variables
    if "target" in x_test.columns:
        x_test = x_test.drop("target", axis=1)

    latest_version = client.get_latest_versions(
        registered_model_name, stages=["None"]
    )[0].version

    clf = mlflow.sklearn.load_model(
        f"models:/{registered_model_name}/{latest_version}"
    )

    predictions = pd.DataFrame(data=clf.predict(x_test), columns=["wine_quality"])

    predictions.to_csv(path_to_predictions_storage / "predictions.csv")
