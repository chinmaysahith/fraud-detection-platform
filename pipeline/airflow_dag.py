"""
Airflow DAG for scheduled fraud model retraining.
Runs every 6 hours and checks for drift before retraining.
"""
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import sys
sys.path.insert(0, '/opt/airflow')

default_args = {
    'owner': 'fraud-detection',
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

def check_drift_task():
    """Check for data drift."""
    from mlops.drift_detector import DriftDetector
    from data.generator import User, TransactionGenerator
    import random

    detector = DriftDetector()
    users = [User(f"user_{i:03d}") for i in range(50)]

    recent_txns = []
    for _ in range(500):
        user = random.choice(users)
        gen = TransactionGenerator(user)
        recent_txns.append(gen.generate_normal())

    result = detector.check_drift(recent_txns)
    print(f"Drift score: {result['drift_score']}")
    return result

def retrain_model_task(**context):
    """Retrain model if drift detected."""
    from mlops.retrainer import ModelRetrainer

    drift_result = context['task_instance'].xcom_pull(task_ids='check_drift')

    if drift_result['drift_score'] > 0.3:
        print("Drift detected. Retraining...")
        retrainer = ModelRetrainer()
        result = retrainer.retrain()
        print(f"Retrain complete: {result}")
    else:
        print("No significant drift. Skipping retraining.")

with DAG(
    'fraud_model_retraining',
    default_args=default_args,
    description='Scheduled fraud model retraining pipeline',
    schedule_interval=timedelta(hours=6),
    start_date=datetime(2024, 1, 1),
    catchup=False,
    tags=['fraud', 'ml', 'retraining']
) as dag:

    check_drift = PythonOperator(
        task_id='check_drift',
        python_callable=check_drift_task,
    )

    retrain_model = PythonOperator(
        task_id='retrain_model',
        python_callable=retrain_model_task,
        provide_context=True,
    )

    check_drift >> retrain_model