import os
from datetime import datetime, timedelta
from airflow import DAG
from airflow.providers.docker.operators.docker import DockerOperator



default_args = {
    'owner': 'E.B.',
    'depends_on_past': False,
    'start_date': datetime(2025, 8, 1),
    'email': ['info@pubmerge.com'],  # Who gets alerts
    'email_on_failure': True,          # Email if task fails
    'email_on_retry': False,           # Email on retries (usually annoying)
    'email_on_success': False,         # Email on success (optional)
    'retries': 3,
    'retry_delay': timedelta(minutes=5)
}

with DAG(
    dag_id="csv_batch_nightly",
    schedule="0 0 * * *",           # 12:00 AM nightly
    default_args=default_args,
    start_date=datetime(2025, 8, 1),
    catchup=False,
    dagrun_timeout=timedelta(hours=2),
) as dag:
    run_batch = DockerOperator(
        task_id="run_csv_batch",
        image="csv-batch:latest",
        force_pull=False,
        docker_url="unix:///var/run/docker.sock",
        network_mode="lambda-inspired-platform_finance-network",
        auto_remove=True,
        do_xcom_push=False,
        mount_tmp_dir=False,
        environment={
            "DB_HOST": os.getenv("DB_HOST"),
            "DB_PORT": os.getenv("DB_PORT", "5432"),
            "DB_NAME": os.getenv("DB_NAME", ""),
            "DB_USER": os.getenv("DB_USER", ""),
            "DB_PASSWORD": os.getenv("DB_PASSWORD", ""),
        },
    )
