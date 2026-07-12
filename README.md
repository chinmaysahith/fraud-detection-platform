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
