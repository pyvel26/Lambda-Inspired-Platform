# Financial Transaction Fraud Detection Platform

A containerized data platform that demonstrates real-time streaming architecture with Kafka, combining batch historical transaction processing with live transaction streaming and fraud detection capabilities.

## Architecture

**Producers (Data Sources):**
- **batch-processor**: Loads historical transaction data from CSV and streams to Kafka
- **producer-streaming-api**: FastAPI service that generates fake live transactions and streams to Kafka

**Message Broker:**
- **kafka**: Central streaming platform that receives all transaction data

**Consumer:**
- **consumer-streaming-api**: FastAPI service that consumes transaction data from Kafka and stores in PostgreSQL

**Storage & Monitoring:**
- **postgres**: Persistent storage for all transaction data
- **pgadmin**: Web-based PostgreSQL administration interface for real-time data monitoring

## Data Flow
CSV Data → batch-processor → Kafka
Fake Data → producer-streaming-api → Kafka
Kafka → consumer-streaming-api → PostgreSQL

## Quick Start

```bash
# Clone and navigate to project
git clone <your-repo>
cd fraud-detection-platform

# Start all services
docker-compose up -d

# Check services are running
docker-compose ps

# Access pgAdmin to monitor data flow
http://localhost:8080

# Monitor Kafka topics (if needed)
docker-compose exec kafka kafka-topics --list --bootstrap-server localhost:9092

Services

Kafka: localhost:9092
PostgreSQL: localhost:5432
pgAdmin: localhost:8080
Producer API: localhost:8001
Consumer API: localhost:8002

Project Structure

fraud-detection-platform/
├── batch-processor/              # CSV to Kafka producer
├── producer-streaming-api/       # Live data generator and Kafka producer  
├── consumer-streaming-api/       # Kafka consumer and PostgreSQL writer
├── data/                         # Transaction CSV files
└── docker-compose.yml            # 6-container orchestration

Technologies

Docker & Docker Compose
Apache Kafka (Confluent Platform)
FastAPI (Python)
PostgreSQL
pgAdmin
Python 3.11

Learning Objectives
Built to practice:

Event-driven architecture with Kafka
Producer/Consumer messaging patterns
Multi-container Docker orchestration
Real-time data streaming platforms
Platform engineering concepts
Microservices separation of concerns

Monitoring
Use pgAdmin to watch transaction data streaming into PostgreSQL in real-time, demonstrating the end-to-end data pipeline functionality.