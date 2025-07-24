import random
from datetime import datetime
from utils import get_db_connection


def generate_next_job_id(conn) -> str:
    """
    Generate the next batch job ID in the format BAT00001, BAT00002, etc.

    Args:
        conn: Active database connection from get_db_connection().

    Returns:
        A new job_id string in the format 'BATxxxxx'.
    """
    cur = conn.cursor()
    cur.execute("SELECT job_id FROM jobs ORDER BY id DESC LIMIT 1;")
    result = cur.fetchone()

    if result and result[0]:
        last_id = result[0]  # e.g., 'BAT00012'
        last_num = int(last_id.replace("BAT", ""))
        next_id = f"BAT{last_num + 1:05d}"
    else:
        next_id = "BAT00001"

    cur.close()
    return next_id


def register_job(conn, job_id: str) -> None:
    """
    Insert a new job record into the jobs table.

    Args:
        conn: Active database connection.
        job_id: The generated job ID to register.
    """
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO jobs (job_id, run_time)
        VALUES (%s, %s)
    """, (job_id, datetime.now()))
    conn.commit()
    cur.close()


def generate_batch_data(job_id: str, count: int = 10000) -> list[dict]:
    """
    Generate a list of fake transaction records for a given job ID.

    Args:
        job_id: The batch job ID to assign to each transaction.
        count: Number of transactions to generate.

    Returns:
        A list of transaction dictionaries.
    """
    transaction_types = ['purchase', 'withdrawal', 'transfer', 'refund', 'deposit']
    categories = ['grocery', 'gas', 'restaurant', 'retail', 'electronics', 'pharmacy', 'coffee', 'entertainment']

    records = []
    for _ in range(count):
        records.append({
            "job_id": job_id,
            "transaction_id": f"TXN-LIVE-{random.randint(1000, 9999)}",
            "account_id": f"ACC-{random.randint(1000, 9999)}",
            "transaction_type": random.choice(transaction_types),
            "amount": round(random.uniform(10.00, 500.00), 2),
            "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            "merchant_category": random.choice(categories),
            "location": "Nashville TN",
            "card_present": True,
            "risk_score": round(random.uniform(0.01, 0.9), 2)
        })

    return records


def save_transactions(conn, records: list[dict]) -> None:
    """
    Insert transaction records into the transactions table.

    Args:
        conn: Active database connection.
        records: List of transaction dictionaries to insert.
    """
    cur = conn.cursor()
    try:
        for record in records:
            cur.execute("""
                INSERT INTO transactions (
                    job_id, transaction_id, account_id, transaction_type,
                    amount, timestamp, merchant_category, location,
                    card_present, risk_score
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (transaction_id) DO NOTHING
            """, (
                record["job_id"],
                record["transaction_id"],
                record["account_id"],
                record["transaction_type"],
                record["amount"],
                record["timestamp"],
                record["merchant_category"],
                record["location"],
                record["card_present"],
                record["risk_score"]
            ))

        conn.commit()
    except Exception as e:
        conn.rollback()
        print(f"[ERROR] Failed to insert transactions: {e}")
        raise
    finally:
        cur.close()


def main() -> None:
    """
    Orchestrates the batch job:
    - Connects to the database
    - Generates a job ID
    - Registers the job
    - Creates batch records
    - Saves records to the database
    Handles errors and rolls back if needed.
    """
    conn = get_db_connection()

    try:
        job_id = generate_next_job_id(conn)
        register_job(conn, job_id)

        records = generate_batch_data(job_id, count=10000)
        save_transactions(conn, records)

    except Exception as e:
        conn.rollback()
        print(f"[ERROR] Batch job failed: {e}")
    finally:
        conn.close()



if __name__ == "__main__":
    main()
