"""
Minimal example of logging model info/metrics with MLflow.
Run this after Person 2 shares their trained model + metrics,
so the model version used in the API is traceable.

Usage: python mlflow_tracking_example.py
"""

import mlflow

mlflow.set_experiment("recommendation-engine")

with mlflow.start_run(run_name="lightgcn-v1"):
    # Example params (replace with real values from Person 2)
    mlflow.log_param("model_type", "LightGCN")
    mlflow.log_param("embedding_dim", 64)
    mlflow.log_param("num_layers", 3)

    # Example metrics (replace with real evaluation results)
    mlflow.log_metric("recall_at_20", 0.34)
    mlflow.log_metric("ndcg_at_20", 0.28)

    # If you have the actual model file:
    # mlflow.pytorch.log_model(model, artifact_path="lightgcn_model")

print("Run logged. Launch the UI with: mlflow ui")
