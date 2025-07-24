import random
from datetime import datetime
from time import sleep
from psycopg2 import OperationalError, IntegrityError
from utils import get_db_connection, get_logger

logger = get_logger("batch_job")


def init_schema(conn):
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS batch_jobs (
            id SERIAL PRIMARY KEY,
            job_id TEXT UNIQUE NOT NULL,
            run_time TIMESTAMP NOT NULL DEFAULT NOW(),
            ingestion_type TEXT NOT NULL DEFAULT 'batch',
            source TEXT NOT NULL DEFAULT 'batch',
            status TEXT DEFAULT 'pending'
        );
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            job_id TEXT NOT NULL,
            transaction_id TEXT PRIMARY KEY,
            account_id TEXT NOT NULL,
            transaction_type TEXT NOT NULL,
            amount NUMERIC(10, 2) NOT NULL,
            event_time TIMESTAMP NOT NULL,
            merchant_category TEXT,
            location TEXT,
            card_present BOOLEAN,
            risk_score NUMERIC(4, 2),
            ingestion_type TEXT DEFAULT 'batch',
            source TEXT DEFAULT 'batch'
        );
    """)
    conn.commit()
    cur.close()
    logger.info("Schema initialized.")


def generate_next_job_id(conn):
    cur = conn.cursor()
    cur.execute("SELECT job_id FROM batch_jobs ORDER BY id DESC LIMIT 1;")
    result = cur.fetchone()
    cur.close()
    if result and result[0]:
        last_num = int(result[0].replace("BAT", ""))
        return f"BAT{last_num + 1:05d}"
    return "BAT00001"


def register_job(conn, job_id, status="pending"):
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO batch_jobs (job_id, ingestion_type, run_time, status)
        VALUES (%s, %s, %s, %s)
    """, (job_id, "batch", datetime.now(), status))
    conn.commit()
    cur.close()
    logger.info(f"Registered job {job_id} with status '{status}'.")


def update_job_status(conn, job_id, status):
    cur = conn.cursor()
    cur.execute("UPDATE batch_jobs SET status = %s WHERE job_id = %s", (status, job_id))
    conn.commit()
    cur.close()
    logger.info(f"Job {job_id} updated to status '{status}'.")


def generate_batch_data(job_id, count=10000):
    transaction_types = ['purchase', 'withdrawal', 'transfer', 'refund', 'deposit']
    categories = ['grocery', 'gas', 'restaurant', 'retail', 'electronics', 'pharmacy', 'coffee', 'entertainment']
    records = []

    for _ in range(count):
        records.append({
            "job_id": job_id,
            "ingestion_type": "batch",
            "transaction_id": f"TXN-LIVE-{random.randint(1000, 9999)}",
            "account_id": f"ACC-{random.randint(1000, 9999)}",
            "transaction_type": random.choice(transaction_types),
            "amount": round(random.uniform(10.00, 500.00), 2),
            "event_time": datetime.now(),
            "merchant_category": random.choice(categories),
            "location": "Nashville TN",
            "card_present": True,
            "risk_score": round(random.uniform(0.01, 0.9), 2)
        })

    return records


def save_transactions(conn, records, job_id):
    cur = conn.cursor()
    failures = 0

    for record in records:
        try:
            cur.execute("""
                INSERT INTO transactions (
                    job_id, ingestion_type, transaction_id, account_id,
                    transaction_type, amount, event_time, merchant_category,
                    location, card_present, risk_score
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (transaction_id) DO NOTHING
            """, (
                record["job_id"], record["ingestion_type"], record["transaction_id"],
                record["account_id"], record["transaction_type"], record["amount"],
                record["event_time"], record["merchant_category"], record["location"],
                record["card_present"], record["risk_score"]
            ))
        except IntegrityError:
            conn.rollback()
            failures += 1
            logger.warning(f"Duplicate transaction ID: {record['transaction_id']}")
        except Exception as e:
            conn.rollback()
            failures += 1
            logger.error(f"Insert failed for {record['transaction_id']}: {e}")

    conn.commit()
    cur.close()
    logger.info(f"{len(records) - failures} inserted, {failures} failed.")


def retry_connection(retries=5, delay=3):
    for attempt in range(retries):
        try:
            conn = get_db_connection()
            logger.info("Connected to database.")
            return conn
        except OperationalError as e:
            logger.warning(f"Retry {attempt + 1}/{retries}: {e}")
            sleep(delay)
    logger.critical("Could not connect to database.")
    return None


def main():
    conn = retry_connection()
    if not conn:
        return

    job_id = None

    try:
        init_schema(conn)
        job_id = generate_next_job_id(conn)
        register_job(conn, job_id, status="started")

        records = generate_batch_data(job_id)
        save_transactions(conn, records, job_id)

        update_job_status(conn, job_id, status="completed")
        logger.info(f"Job {job_id} completed.")

    except Exception as e:
        logger.error(f"Fatal error: {e}")
        if job_id:
            update_job_status(conn, job_id, status="failed")
            conn.rollback()
    finally:
        conn.close()


if __name__ == "__main__":
    main()
