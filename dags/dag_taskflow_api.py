from airflow.decorators import dag, task
from datetime import datetime, timedelta
from airflow.operators.python import PythonOperator


default_args={
    'owner': 'Aditya',
    'retries': 5,
    'retry_delay': timedelta(minutes=5)
}

@dag(default_args=default_args,
    dag_id='dag_taskflow_api_v2',
    description='DAG with taskflow API',
    start_date=datetime(2023,3,3),
    schedule_interval='@daily')
def hello_world_etl():

    @task(multiple_outputs=True)
    def get_name():
        return {
            'firstname':'Aditya',
            'lastname':'Prasetyo'
        }

    @task 
    def get_age():
        return '24'

    @task
    def greet(firstname,lastname,age):
        print(f'Hello World! My name is {firstname} {lastname} and I am {age} years old')
    
    name=get_name()
    age=get_age()
    greet(name['firstname'],name['lastname'],age)

greet_etl=hello_world_etl()
