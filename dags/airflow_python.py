from airflow import DAG
from datetime import timedelta,datetime
from airflow.operators.python import PythonOperator



defaults_args={
    'owner': 'aditya',
    'retries': 5,
    'retry_delay': timedelta(minutes=5)
}

def greet(ti):
    firstname=ti.xcom_pull(task_ids='get_name', key='firstname')
    lastname=ti.xcom_pull(task_ids='get_name', key='lastname')
    age=ti.xcom_pull(task_ids='get_age', key='age')
    print(f'Hello world! My name is {firstname} {lastname} and I am {age} years old')

def get_name(ti):
    ti.xcom_push(key='firstname', value='Aditya')
    ti.xcom_push(key='lastname', value='Prasetyo')

def get_age(ti):
    ti.xcom_push(key='age',value='24')


with DAG(
    default_args=defaults_args,
    dag_id='dag_python_operator_v5',
    description='DAG with python operator',
    start_date=datetime(2023,3,3),
    schedule_interval='@daily'
) as dag :
    task1=PythonOperator(
        task_id='greet',
        python_callable=greet
        # op_kwargs={
        #     'age': '24'
        # }
    )

    task2=PythonOperator(
        task_id='get_name',
        python_callable=get_name,

    )
    task3=PythonOperator(
        task_id='get_age',
        python_callable=get_age
    )

    task1 << [task2, task3]