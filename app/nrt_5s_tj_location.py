import airflow
from airflow import DAG
from airflow.operators import BashOperator
from datetime import timedelta
default_args = {
    'owner': 'Airflow',
    'depends_on_past': False,
    'start_date': airflow.utils.dates.days_ago(2),
    'email': ['airflow@example.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(seconds=20)
}
dag1 = DAG(
    'nrt_tj_stream', default_args=default_args, schedule_interval=timedelta(seconds=5))

bash_task = BashOperator(
    task_id='5s_tracking_data',
    bash_command='python /usr/local/airflow/dags/app.py',
    dag=dag1
)

