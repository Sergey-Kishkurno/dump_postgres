from datetime import datetime
# import downloader

from airflow import DAG
from airflow.operators.bash_operator import BashOperator


default_args = {
    'owner': 'airflow',
    'email': ['airflow@airflow.com'],
    'email_on_failure': False,
    'retries': 2
}


dag = DAG (
    '001_dag_downloader',
    schedule_interval='@hourly',
    start_date=datetime(2022, 1, 28, 1, 0),
    end_date=datetime(2022, 1, 28, 1, 0),
    default_args=default_args
)


t1 = BashOperator(
    task_id='dump_postgres',
    bash_command='python3 -m downloader',
    dag=dag
)