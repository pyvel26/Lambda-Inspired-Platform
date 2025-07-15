# Real-time Data Platform

A containerized data platform that demonstrates real-time streaming architecture using Kafka, combining batch historical processing with live transaction streams. Data flows through Kafka into PostgreSQL, where it can be monitored in real-time.

---

## Architecture

**Producers (Data Sources):**

- **batch-processor**: Loads historical transaction data from CSV files and streams to Kafka
- **producer-streaming-api**: Python-based service that generates fake live transactions and streams to Kafka

**Message Broker:**

- **kafka**: Central streaming platform that receives all transaction data

**Consumer:**

- **consumer-streaming-api**: Python-based service that consumes transaction data from Kafka and writes to PostgreSQL

**Storage & Monitoring:**

- **postgres**: Persistent storage for all transaction data
- **pgadmin**: Web-based PostgreSQL interface for real-time monitoring

---

## Data Flow

- CSV Data → `batch-processor` → Kafka
- Fake Data → `producer-streaming-api` → Kafka
- Kafka → `consumer-streaming-api` → PostgreSQL

---

## 🛡 Infrastructure Layer Overview

Host machine: **AMD Ryzen 7 5800H — 8 physical cores / 16 logical cores, 16 GB RAM**\
Total project usage: **12.25 logical cores**, **≈10.5 GB RAM**

Each container in this setup is capped with CPU and memory limits to avoid overloading the system during streaming and batch processing. These limits were configured to mimic real-world infrastructure behavior, even though this is a self-guided learning project.

> This is an early project built while learning container orchestration and system resource management. The goal was to treat the environment like production from the start — even before gaining real-world experience.

#### Resource Allocation

| Container              | CPU Limit | Memory Limit |
| ---------------------- | --------- | ------------ |
| kafka                  | 2.0       | 2g           |
| producer-streaming-api | 3.0       | 2g           |
| batch-processor        | 1.5       | 1g           |
| consumer-streaming-api | 4.0       | 2.5g         |
| postgres               | 1.5       | 2g           |
| pgadmin                | 0.25      | 512m         |
| **Total**              | **12.25** | **≈10.5 GB** |

---

## Quick Start

```bash
# Clone and navigate to project
git clone <your-repo>
cd real-time-data_platform

# Start all services
docker-compose up -d

# Check services are running
docker-compose ps

# Access pgAdmin to monitor data
http://localhost:8080

# (Optional) List Kafka topics
docker-compose exec kafka kafka-topics --list --bootstrap-server localhost:9092
```

---

## Services

- Kafka: `localhost:9092`
- PostgreSQL: `localhost:5432`
- pgAdmin: `localhost:8080`
- Producer API: `localhost:8001`
- Consumer API: `localhost:8002`

---

## Project Structure

```
real-time-data_platform/
├── batch-processor/              # CSV to Kafka producer
├── producer-streaming-api/       # Live data generator and Kafka producer  
├── consumer-streaming-api/       # Kafka consumer and PostgreSQL writer
├── data/                         # Transaction CSV files
└── docker-compose.yml            # 6-container orchestration
```

---

## Technologies

- Docker & Docker Compose
- Apache Kafka (Confluent Platform)
- Python 3.11
- PostgreSQL
- pgAdmin

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

## Monitoring

Use pgAdmin to observe transaction data arriving in real-time, validating the full end-to-end data pipeline from producer to database.

