"""
Trainer module for the Isolation Forest model.
Generates normal transaction data and trains the model.
"""

import os
import sys
from typing import List

import joblib
import mlflow
import mlflow.sklearn
from sklearn.ensemble import IsolationForest

# Add the root directory to sys.path to import data modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from data import config
from data.generator import User, TransactionGenerator
from model.features import extract_features

class ModelTrainer:
    """
    Handles generating training data and training the Isolation Forest model.
    """

    def generate_training_data(self, n_samples: int) -> List[List[float]]:
        """
        Generates normal transactions for training and returns their feature vectors.
        """
        features_list = []
        # Generate transactions in a loop until we hit n_samples
        for i in range(n_samples):
            # Create a user with a unique ID
            user = User(f"user_train_{i}")
            generator = TransactionGenerator(user)
            # Generate a normal transaction
            txn = generator.generate_normal()
            # Extract features
            features = extract_features(txn)
            features_list.append(features)

        return features_list

    def train(self, n_samples: int = config.TRAINING_SAMPLES) -> IsolationForest:
        """
        Generates training data, trains the Isolation Forest model, and saves it to disk.
        """
        print(f"Training on {n_samples:,} samples...")

        # Generate data
        X = self.generate_training_data(n_samples)

        # Initialize model
        model = IsolationForest(
            contamination=config.CONTAMINATION,
            random_state=42
        )

        try:
            mlflow.set_tracking_uri(config.MLFLOW_TRACKING_URI)
            mlflow.set_experiment(config.MLFLOW_EXPERIMENT_NAME)

            with mlflow.start_run(run_name="isolation-forest-training"):
                model.fit(X)

                # Log parameters
                mlflow.log_param("n_samples", n_samples)
                mlflow.log_param("contamination", config.CONTAMINATION)
                mlflow.log_param("random_state", 42)

                # Log metrics
                mlflow.log_metric("training_samples", n_samples)
                mlflow.log_metric("n_features", len(config.FEATURE_COLUMNS))

                # Log model to registry
                mlflow.sklearn.log_model(
                    model,
                    "isolation-forest",
                    registered_model_name=config.MODEL_NAME
                )
                print(f"Model logged to MLflow: {config.MLFLOW_EXPERIMENT_NAME}")
        except Exception as e:
            print(f"MLflow tracking failed, saving locally only. Error: {e}")
            model.fit(X)

        # Save model locally
        os.makedirs(os.path.dirname(config.MODEL_PATH), exist_ok=True)
        joblib.dump(model, config.MODEL_PATH)

        print(f"Model saved to {config.MODEL_PATH}")
        return model

if __name__ == "__main__":
    trainer = ModelTrainer()
    trainer.train()
