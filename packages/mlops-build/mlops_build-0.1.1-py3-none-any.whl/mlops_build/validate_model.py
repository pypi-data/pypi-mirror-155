# -*- coding: utf-8 -*-
import os
import json
import mlflow
import pandas as pd
from pathlib import Path
from mlflow.tracking.client import MlflowClient
from sklearn.metrics import (
    precision_score,
    recall_score,
    roc_auc_score,
    roc_curve
)


def main(
        path_to_dataset: str,
        path_to_metrics_storage: str,
        registered_model_name: str,
        experiment_name: str,
        dagshub_mlflow_tracking_uri: str,
        mlflow_tracking_username: str,
        mlflow_tracking_password: str,
) -> None:
    """
    Runs validation method
    Args:
        path_to_dataset: absolute path to your dataset
        path_to_metrics_storage: absolute path to your metrics storage
        experiment_name: the name of the experiment for mlflow
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

    if experiment_name is None:

        experiments = client.list_experiments()
        current_experiment = experiments[-1]
        df = mlflow.search_runs([current_experiment.experiment_id])
        df.sort_values(by="start_time", inplace=True)
        run_id = df.run_id.values[-2]

    else:
        current_experiment = mlflow.get_experiment_by_name(experiment_name)
        df = mlflow.search_runs([current_experiment.experiment_id])
        run_id = df.run_id.values[-2]

    with mlflow.start_run(run_id=run_id):
        path_to_dataset = Path(path_to_dataset)
        path_to_metrics_storage = Path(path_to_metrics_storage)

        # read dataset
        test = pd.read_csv(path_to_dataset).drop(columns=["Unnamed: 0"])

        # Now separate the dataset as response variable and feature variables
        x_test = test.drop("target", axis=1)
        y_test = test["target"]

        latest_version = client.get_latest_versions(
            registered_model_name, stages=["None"]
        )[0].version

        clf = mlflow.sklearn.load_model(
            f"models:/{registered_model_name}/{latest_version}"
        )

        predictions = clf.predict(x_test)
        predictions_proba = clf.predict_proba(x_test)

        # Let's see how our model performed
        precision = precision_score(y_test.values, predictions)
        recall = recall_score(y_test.values, predictions)
        roc_auc = roc_auc_score(y_test.values, predictions_proba[:, 1])

        mlflow.log_metrics({"test_precision": precision})
        mlflow.log_metrics({"test_recall": recall})
        mlflow.log_metrics({"test_roc_auc": roc_auc})

        fpr, tpr, _ = roc_curve(y_test.values, predictions_proba[:, 1])

        metrics = {
            "train": {
                "precision": precision,
                "recall": recall,
                "roc_auc": roc_auc,
            }
        }

        plots = {"train": [{"tpr": i, "fpr": j} for i, j in zip(tpr, fpr)]}

        with open(str(path_to_metrics_storage / "metrics.json"), "w") as handler:
            json.dump(metrics, handler)

        with open(str(path_to_metrics_storage / "plots.json"), "w") as handler:
            json.dump(plots, handler)
