from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta

default_args = {
    "retries": 1,
    "retry_delay": timedelta(minutes=1),
}

with DAG(
    dag_id="etl_variant_13",
    start_date=datetime(2026, 3, 1),
    schedule="*/5 * * * *",
    catchup=False,
    default_args=default_args,
) as dag:

    extract = BashOperator(
        task_id="extract",
        bash_command="""
        echo 'START EXTRACT' &&
        python /opt/airflow/project/src/extract.py &&
        echo 'END EXTRACT'
        """
    )

    transform = BashOperator(
        task_id="transform",
        bash_command="""
        echo 'START TRANSFORM' &&
        python /opt/airflow/project/src/mart.py &&
        echo 'END TRANSFORM'
        """
    )

    load = BashOperator(
        task_id="load",
        bash_command="""
        echo 'START LOAD' &&
        python /opt/airflow/project/src/load.py &&
        echo 'END LOAD'
        """
    )

    dq = BashOperator(
        task_id="dq",
        bash_command="""
        echo 'START DQ' &&
        python /opt/airflow/project/src/dq.py &&
        echo 'END DQ'
        """
    )

    extract >> transform >> load >> dq
