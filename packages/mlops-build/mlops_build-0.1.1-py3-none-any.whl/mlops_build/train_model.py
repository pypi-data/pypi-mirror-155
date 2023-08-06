# -*- coding: utf-8 -*-
import os
import shap
import yaml
import mlflow
import optuna
import pandas as pd
from pathlib import Path
from functools import partial
from matplotlib import pyplot as plt
from mlflow.models import infer_signature
from mlflow.tracking.client import MlflowClient
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_score


def objective(
        trial,
        params: dict,
        x_train: pd.DataFrame,
        y_train: pd.DataFrame
) -> float:
    """
    Objective function for optuna optimization
    Args:
        trial: optuna object
        params: run params
        x_train: features
        y_train: target

    Returns:
        target: the value of the metric
    """

    with mlflow.start_run(nested=True):
        penalty = trial.suggest_categorical("penalty", params["penalty"])
        c = trial.suggest_float(
            "C",
            float(params["C"]["upper_bound"]),
            float(params["C"]["lower_bound"]),
            log=True,
        )

        clf = LogisticRegression(solver="liblinear", penalty=penalty, C=c)

        mlflow.log_params({"C": c, "penalty": penalty})

        target = cross_val_score(
            clf, x_train, y_train, n_jobs=-1, cv=3, scoring="precision"
        ).mean()

        mlflow.log_metrics({"train_precision": target})

    return target


def main(
        path_to_dataset: str,
        path_to_params_search_space: str,
        path_to_save_artifacts: str,
        experiment_name: str,
        registered_model_name: str,
        dagshub_mlflow_tracking_uri: str,
        mlflow_tracking_username: str,
        mlflow_tracking_password: str,
) -> None:
    """
    Runs training job and save best model to model's storage
    Args:
        path_to_dataset: absolute path to your dataset
        path_to_params_search_space: absolute path to your yaml files with search params
        path_to_save_artifacts: absolute path to your artifact storage
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
    mlflow.set_experiment(experiment_name)

    with mlflow.start_run() as run:

        experiment_id = run.info.experiment_id

        path_to_dataset = Path(path_to_dataset)
        path_to_params_search_space = Path(path_to_params_search_space)
        path_to_save_artifacts = Path(path_to_save_artifacts)

        # read dataset
        train = pd.read_csv(path_to_dataset).drop(columns=["Unnamed: 0"])

        # Now separate the dataset as response variable and feature variables
        x_train = train.drop("target", axis=1)
        y_train = train["target"]

        # params space
        with open(path_to_params_search_space / "params.yaml", "r") as stream:
            params = yaml.safe_load(stream)["train"]

        obj_partial = partial(
            objective, params=params, x_train=x_train, y_train=y_train
        )

        study = optuna.create_study(direction="maximize")
        study.optimize(obj_partial, n_trials=200)

        # find the best run, log its metrics as the final metrics of this run.
        client = MlflowClient()
        runs = client.search_runs(
            [experiment_id],
            "tags.mlflow.parentRunId = '{run_id}' ".format(run_id=run.info.run_id),
        )

        best_metric = 0
        best_run = None
        for r in runs:
            if r.data.metrics["train_precision"] > best_metric:
                if best_run is not None:
                    run_id = best_run.info.run_id
                    mlflow.delete_run(run_id)
                best_run = r
                best_metric = r.data.metrics["train_precision"]
            else:
                run_id = r.info.run_id
                mlflow.delete_run(run_id)
        mlflow.set_tag("params_search_best_run", best_run.info.run_id)

        mlflow.log_metrics(
            {
                "train_precision": best_metric,
            }
        )

        mlflow.log_params(
            {"C": best_run.data.params["C"], "penalty": best_run.data.params["penalty"]}
        )

        # Let's run SVC again with the best parameters.
        clf = LogisticRegression(solver="liblinear", **study.best_trial.params)
        clf.fit(x_train, y_train)

        signature = infer_signature(x_train, y_train)

        # Log the sklearn model and register as version 1
        mlflow.sklearn.log_model(
            sk_model=clf,
            artifact_path="sklearn-model",
            registered_model_name=registered_model_name,
            signature=signature,
        )

        explainer = shap.Explainer(clf.predict, x_train)
        shap_values = explainer(x_train)

        # summarize the effects of all the features
        shap.plots.beeswarm(shap_values, show=False)
        plt.savefig(
            path_to_save_artifacts / "reports/features_importance/shap_values.png",
            format="png",
            dpi=150,
            bbox_inches="tight",
        )

        mlflow.log_artifact(
            str(path_to_save_artifacts / "reports/features_importance/shap_values.png")
        )
