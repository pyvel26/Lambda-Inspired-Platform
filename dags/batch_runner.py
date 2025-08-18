from datetime import datetime, timedelta
from airflow import DAG
from airflow.providers.docker.operators.docker import DockerOperator

with DAG(
    dag_id="csv_batch_nightly",
    schedule="0 0 * * *",                 # 12:00 AM every day
    start_date=datetime(2025, 8, 1),
    catchup=False,
    dagrun_timeout=timedelta(hours=2),
) as dag:
    run_batch = DockerOperator(
        task_id="run_csv_batch",
        image="csv-batch:latest",         # <-- your image name:tag
        command="python /app/jobs/csv_batch.py --mode batch",  # or omit if CMD handles it
        docker_url="unix://var/run/csv_batch_nightly.sock",
        network_mode="yourproject_default",  # <-- your compose network
        auto_remove=True,
        do_xcom_push=False,
    )

