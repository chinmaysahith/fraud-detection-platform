# fraud-detection-platform

## Phase 2 — Kafka Setup

### Start Kafka
```bash
docker-compose up -d
```

### Verify Kafka is running
```bash
docker ps
```

### Run the stream (sends to Kafka + console)
```bash
python data/stream.py
```

### Verify messages arriving in Kafka (new terminal)
```bash
python data/kafka_consumer.py
```

### Stop Kafka
```bash
docker-compose down
```

## Phase 3 — ML Model

### Train the model first
```bash
python model/trainer.py
```

### Start the stream (Terminal 1)
```bash
python data/stream.py
```

### Start inference consumer (Terminal 2)
```bash
python model/inference_consumer.py
```

## Phase 4 — PostgreSQL Storage

### Start all services (Kafka + PostgreSQL)
```bash
docker-compose up -d
```

### Verify PostgreSQL is running
```bash
docker ps
```

### Install database dependency
```bash
pip install psycopg2-binary
```

### Train model (if not already done)
```bash
python model/trainer.py
```

### Terminal 1 — Start stream
```bash
python data/stream.py
```

### Terminal 2 — Start inference + saving
```bash
python model/inference_consumer.py
```

### Verify data is being saved
```bash
docker exec -it postgres psql -U fraud_user -d fraud_detection -c "SELECT COUNT(*) FROM transactions;"
docker exec -it postgres psql -U fraud_user -d fraud_detection -c "SELECT * FROM fraud_alerts ORDER BY created_at DESC LIMIT 5;"
```

## Phase 5 — Grafana Dashboard

### Start all services
```bash
docker-compose up -d
```

### Open Grafana
- URL: http://localhost:3000
- Username: admin
- Password: admin

### Navigate to dashboard
- Left sidebar → Dashboards → Fraud Detection → Fraud Detection Platform

### Run the pipeline
```bash
# Terminal 1
python data/stream.py

# Terminal 2
python model/inference_consumer.py
```

Watch the dashboard update every 5 seconds in real time.

## Phase 6 — MLOps

### Start all services
```bash
docker-compose up -d
```

### Install MLOps dependencies
```bash
pip install evidently mlflow
```

### Train model with MLflow tracking
```bash
python model/trainer.py
```

### View MLflow experiments
- URL: http://localhost:5000
- See all model versions, parameters, metrics

### View Airflow DAGs
- URL: http://localhost:8080
- Username: admin / Password: admin
- Find DAG: fraud_model_retraining
- Enable and trigger manually to test

### Run pipeline with drift detection
```bash
# Terminal 1
python data/stream.py

# Terminal 2
python model/inference_consumer.py
# Watch for drift check every 500 transactions
```

## Phase 7 — FastAPI

### Install dependencies
```bash
pip install fastapi uvicorn pydantic
```

### Run API locally
```bash
python -m uvicorn api.main:app --reload --port 8000
```

### Interactive API docs
- URL: http://localhost:8000/docs
- Click any endpoint → Try it out → Add API key → Execute

### API Key
Add to every request header:
```
X-API-Key: fraud-api-key-x7k9m2p4
```

### Example predict request
```bash
curl -X POST http://localhost:8000/predict \
  -H "X-API-Key: fraud-api-key-x7k9m2p4" \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "user_042",
    "amount": 12000,
    "location": "Nigeria",
    "merchant": "weapons",
    "device": "laptop",
    "time_of_day": "midnight",
    "day_of_week": "Monday"
  }'
```

### Expected response
```json
{
  "txn_id": "abc-123",
  "fraud_score": 0.94,
  "label": "FRAUD",
  "is_fraud_predicted": true
}
```
