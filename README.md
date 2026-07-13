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
