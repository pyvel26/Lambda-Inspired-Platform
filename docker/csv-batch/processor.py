import random
from datetime import datetime
from psycopg2 import IntegrityError
from utils import get_db_connection, get_logger

logger = get_logger("csv_batch")


def generate_next_job_id(cur):
    """Generate sequential BAT job ID for tracking batch runs"""
    cur.execute("SELECT job_id FROM batch_jobs ORDER BY id DESC LIMIT 1;")
    result = cur.fetchone()

    if result and result[0]:
        last_num = int(result[0].replace("BAT", ""))
        return f"BAT{last_num + 1:05d}"
    return "BAT00001"


def register_job(cur, job_id, status="pending"):
    """Register new batch job in tracking table"""
    cur.execute("""
        INSERT INTO batch_jobs (job_id, run_time, status)
        VALUES (%s, %s, %s)
    """, (job_id, datetime.now(), status))
    logger.info(f"Registered job {job_id} with status '{status}'.")


def update_job_status(cur, job_id, status):
    """Update job status for monitoring and audit"""
    cur.execute("UPDATE batch_jobs SET status = %s WHERE job_id = %s", (status, job_id))
    logger.info(f"Job {job_id} updated to status '{status}'.")


def generate_batch_data(job_id, count=10000):
    """Generate realistic transaction data for batch processing"""
    transaction_types = ['purchase', 'withdrawal', 'transfer', 'refund', 'deposit']
    categories = ['grocery', 'gas', 'restaurant', 'retail', 'electronics', 'pharmacy', 'coffee', 'entertainment']
    records = []

    for _ in range(count):
        records.append({
            "job_id": job_id,
            "transaction_id": f"TXN-{random.randint(1000, 9999)}",  # Shortened from TXN-LIVE-####
            "account_id": f"ACC-{random.randint(1000, 9999)}",
            "transaction_type": random.choice(transaction_types),
            "amount": round(random.uniform(10.00, 500.00), 2),
            "event_time": datetime.now(),
            "merchant_category": random.choice(categories),
            "location": "Nashville TN",
            "card_present": True,
            "risk_score": round(random.uniform(0.01, 0.9), 2),
            "ingestion_type": "batch"
        })

    return records


def save_transactions(cur, records):
    """Insert transactions with individual error handling for data integrity"""
    failures = 0

    for record in records:
        try:
            cur.execute("""
                INSERT INTO transactions (
                    job_id, transaction_id, account_id, transaction_type,
                    amount, event_time, merchant_category, location,
                    card_present, risk_score, ingestion_type
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (transaction_id) DO NOTHING
            """, (
                record["job_id"], record["transaction_id"], record["account_id"],
                record["transaction_type"], record["amount"], record["event_time"],
                record["merchant_category"], record["location"],
                record["card_present"], record["risk_score"],
                record["ingestion_type"]
            ))
        except IntegrityError:
            failures += 1
            logger.warning(f"Duplicate transaction ID: {record['transaction_id']}")
        except Exception as e:
            failures += 1
            logger.error(f"Insert failed for {record['transaction_id']}: {e}")

    logger.info(f"{len(records) - failures} inserted, {failures} failed.")


def main():
    """Main batch processing workflow - runs nightly at midnight"""
    conn = None
    job_id = None

    try:
        # Connect to database
        conn = get_db_connection()
        cur = conn.cursor()
        logger.info("Connected to database.")

        # Generate unique job ID for this batch run
        job_id = generate_next_job_id(cur)
        register_job(cur, job_id, status="started")
        conn.commit()

        # Generate and process batch data (10K records for nightly run)
        logger.info(f"Generating batch data for job {job_id}")
        records = generate_batch_data(job_id)

        # Save transactions with individual error handling
        save_transactions(cur, records)

        # Mark job as completed
        update_job_status(cur, job_id, status="completed")
        conn.commit()
        logger.info(f"Job {job_id} completed successfully.")

    except Exception as e:
        logger.error(f"Fatal error in job {job_id}: {e}")
        if conn and job_id:
            try:
                cur = conn.cursor()
                update_job_status(cur, job_id, status="failed")
                conn.commit()
            except:
                pass  # Don't fail on failure logging

    finally:
        if conn:
            conn.close()


if __name__ == "__main__":
    main()