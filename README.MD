# Lambda Data Platform
This platform demonstrates Lambda architecture using an 8-container system that combines real-time streaming with scheduled batch processing. Stream data flows through Kafka while batch data is processed directly to PostgreSQL with job tracking and monitoring.
---

## Architecture

## Platform Components (8 Containers)

### Real-time Stream Processing:
- **lambda-producer-ctr**: Generates live transaction data and streams to Kafka
- **kafka**: Message broker for real-time transaction streaming
- **lambda-consumer-ctr**: Consumes Kafka streams and writes to PostgreSQL

### Scheduled Batch Processing:
- **lambda-airflow-ctr**: Schedules batch jobs nightly at midnight
- **lambda-csv-batch-ctr**: Generates batch transaction data with job tracking

### Data Management:
- **lambda-postgres-ctr**: PostgreSQL database for transaction storage
- **lambda-pgadmin-ctr**: Database management and monitoring interface
- **lambda-db-setup-ctr**: Schema initialization (runs once, exits)
---

## Data Flow

### Stream Path:
Live Data → lambda-producer-ctr → Kafka → lambda-consumer-ctr → PostgreSQL

### Batch Path:
Nightly Schedule (midnight) → lambda-airflow-ctr → lambda-csv-batch-ctr → PostgreSQL

### Management:
lambda-db-setup-ctr → PostgreSQL Schema
pgAdmin → PostgreSQL Monitoring
---

## 🛡 Infrastructure Layer Overview

My Host machine: **AMD Ryzen 7 5800H — 8 physical cores / 16 logical cores, 16 GB RAM**\
Total project usage: **11 logical cores**, **≈13 GB RAM**

Each container in this setup is capped with CPU and memory limits to avoid overloading the system during streaming and batch processing. These limits were configured to mimic real-world infrastructure behavior, even though this is a self-guided learning project.

> This is an early project built while learning container orchestration and system resource management. The goal was to treat the environment like production from the start — even before gaining real-world experience.

#### Resource Allocation
| Container | CPU Limit | Memory Limit | Purpose                 |
|-----------|-----------|--------------|-------------------------|
| kafka | 4.0 | 2g | Message streaming       |
| lambda-producer-ctr | 1.0 | 2g | Stream data generation  |
| lambda-consumer-ctr | 4.0 | 2g | Stream processing       |
| lambda-csv-batch-ctr | 0.25 | 1g | Batch processing        |
| lambda-airflow-ctr | 0.25 | 1g | Trigger Batch Container |
| lambda-postgres-ctr | 1.0 | 4g | Database storage        |
| lambda-pgadmin-ctr | 0.25 | 512m | DB management           |
| lambda-db-setup-ctr | 0.25 | 512m | Schema setup            |
| **Total** | **~11 cores** | **~13 GB** | **8 containers**        |
---


## Key Features

### Data Processing:
- **Real-time streaming** with Kafka producer/consumer pattern
- **Scheduled batch processing** with airflow workflow automation
- **Job tracking** with status monitoring (pending → running → completed)
- **Data lineage** with transaction ID preservation from source systems

### Architecture:
- **Lambda pattern** combining stream and batch processing
- **Container orchestration** with Docker Compose
- **Service networking** with isolated container communication
- **Database schema management** with automated setup


## Quick Start

```bash
# Clone and navigate to project
git clone https://github.com/pyvel26/Lambda-Inspired-Platform
cd Lambda-Inspired-Platform

# Setup environment variables
cp .env.example .env
# Edit .env and fill in your database credentials

# Start all services
docker compose up -d

# Check services are running
docker compose ps

# Access pgAdmin to monitor batch-datasource
http://localhost:8080

# (Optional) List Kafka topics
docker compose exec kafka kafka-topics --list --bootstrap-server localhost:9092
```

---

## Services

- pgAdmin: localhost:8080 (admin@admin.com / admin)
- PostgreSQL: localhost:5432
- Kafka: localhost:9092
---

## Project Structure

```
Lambda-Inspired-Platform/
├── data/                  # CSV files for batch processing
├── docker/                # Container configurations  
├── logs/                  # Application logs
├── output/                # Processing outputs
├── docker-compose.yml     # 8-container orchestration
├── main.py               # Main application entry
├── utils.py              # Shared utilities
└── README.md

---

## Technologies

- Docker & Docker Compose
- Apache Kafka (Confluent Platform)
- Python 3.11
- PostgreSQL
- pgAdmin
- Airflow

---

## Learning Objectives

Built to practice:

- Event-driven architecture using Kafka
- Producer/Consumer messaging patterns
- Multi-container Docker orchestration
- Real-time streaming systems
- Platform engineering discipline (resource control, networking)
- Microservice separation of concerns

---
## Monitoring Commands

# Check container resource usage
docker stats

# View streaming data
docker logs lambda-consumer-ctr -f

# Check batch job status
docker logs lambda-airflow-ctr -f

Use pgAdmin to observe transaction data arriving in real-time, validating the full end-to-end data pipeline from producer to database.


## Common Issues
- **Airflow "Permission denied"**: Run `sudo chown -R $USER:$USER airflow-home/`
- **Kafka connection fails**: Wait 30-60 seconds for Kafka to fully start
- **Docker socket errors**: Ensure user is in docker group