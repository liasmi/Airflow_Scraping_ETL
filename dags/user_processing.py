from datetime import datetime,timedelta
from airflow import DAG
from airflow.decorators import task
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.providers.http.sensors.http import HttpSensor
from airflow.providers.http.operators.http import SimpleHttpOperator
from airflow.providers.sqlite.operators.sqlite import SqliteOperator
from airflow.operators.python import PythonOperator
from scripts.create_table import create_table_sql
from scripts.book_scrap import scrap_info

def check(response):
    if response == 200:
        print("Returning True")
        return True
    else:
        print("Returning False")
        return False

default_args = {
    'owner': 'ismailox',
    'depends_on_past': False,
    'start_date': datetime(2023, 1, 1),
    'email': ['ismailox94@gmail.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
    'schedule':"None",
    'max_active_runs':1,
}


with DAG('user_processing',default_args=default_args,catchup=False,tags=["ismail's"],) as dag:
    
    create_table=PostgresOperator(
        task_id='create_table',
        postgres_conn_id='postgres',
        sql='''
            CREATE TABLE IF NOT EXISTS users (
                firstname TEXT NOT NULL,
                lastname TEXT NOT NULL,
                country TEXT NOT NULL,
                username TEXT NOT NULL,
                password TEXT NOT NULL,
                email TEXT NOT NULL
            );
        
        '''

    )

 
    table_sql= PythonOperator(
        task_id='table',
        python_callable=create_table_sql
    )
    etl_job_book= PythonOperator(
        task_id='etl_job_book',
        python_callable=scrap_info
    )

    is_api_available= HttpSensor(
        task_id='is_api_available',
        http_conn_id='user_api',
        endpoint='https://httpbin.org/get'
    )
    check_url = SimpleHttpOperator(
     task_id='check_url',
     http_conn_id='c2c_test',
     method='Get',
     endpoint='',
     response_check=lambda response: True if check(response.status_code) is True else False

)



    check_url>>table_sql>>etl_job_book
