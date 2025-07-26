import sys
from utils import get_logger, get_db_connection

logger = get_logger("db-init")


def create_required_tables():
    """Create all required tables with proper schema"""
    try:
        conn = get_db_connection()
        cur = conn.cursor()

        # Create batch_jobs table
        logger.info("Creating table: batch_jobs")
        cur.execute("""
            CREATE TABLE IF NOT EXISTS batch_jobs (
            id SERIAL PRIMARY KEY,
            job_id TEXT UNIQUE NOT NULL,
            run_time TIMESTAMP NOT NULL DEFAULT NOW(),
            status TEXT DEFAULT 'pending'
        );
        """)

        # Create transactions table
        logger.info("Creating table: transactions")
        cur.execute("""
            CREATE TABLE IF NOT EXISTS transactions (
                job_id TEXT,
                transaction_id TEXT PRIMARY KEY,
                account_id TEXT NOT NULL,
                transaction_type TEXT NOT NULL,
                amount NUMERIC(10, 2) NOT NULL,
                event_time TIMESTAMP NOT NULL,
                merchant_category TEXT,
                location TEXT,
                card_present BOOLEAN,
                risk_score NUMERIC(4, 2),
                ingestion_type TEXT DEFAULT 'STREAM'
            );
        """)

        conn.commit()
        logger.info("Database setup completed successfully")
        return True

    except Exception as e:
        logger.error(f"Database setup failed: {e}")
        return False
    finally:
        if 'conn' in locals():
            conn.close()


if __name__ == "__main__":
    success = create_required_tables()
    sys.exit(0 if success else 1)