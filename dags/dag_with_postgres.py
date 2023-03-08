from airflow import DAG 
from datetime import timedelta,datetime 
from airflow.providers.postgres.operators.postgres import PostgresOperator



default_args={
    'owner': 'Aditya',
    'retries': 5,
    'retry_delay':timedelta(minutes=5)
}

with DAG(
    dag_id='dag_postgrest_v3',
    default_args=default_args,
    description = 'DAG with Postgres',
    start_date=datetime(2023,3,7),
    schedule_interval='@daily'
) as dag:
    task1=PostgresOperator(
        task_id='create_postgres_table',
        postgres_conn_id='postgrest_localhost',
        sql='''
        create table if not exists dag_run (
            dt date,
            dag_id character varying,
            primary key (dt, dag_id)
        )
        '''
    )

    task2=PostgresOperator(
        task_id='insert_table',
        postgres_conn_id='postgrest_localhost',
        sql='''
        insert into dag_run (dt,dag_id) values('{{ ds }}','{{dag.dag_id}}')
        '''
    )

    task3=PostgresOperator(
        task_id='delete_data_table',
        postgres_conn_id='postgrest_localhost',
        sql='''
        delete from dag_run where dt = '{{ ds }}' and dag_id = '{{dag.dag_id}}'
        '''
    )

    task1 >> task3 >> task2
