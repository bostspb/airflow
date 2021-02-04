"""
Задание:
1. Все функции вынесены в отдельный модуль и в DAG файле только сама структура графа (директория модулей должна быть в PATH)
2. Отказ от работы с локальными файлами:
    - сначала скачанный датасет пушится в XCom (он весит ~50 КБ)
    - затем он пуллится из XCom и передается двум преобразованиям (pivot и mean_fare)
3. Результаты преобразований записываются в две таблицы локальной базы PostgreSQL (Connections+Hooks или psycopg2/sqlalchemy).
4. Имена таблиц в PostgreSQL заданы в Variables
"""

import os
import sys
import datetime as dt
from airflow.models import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from airflow.providers.postgres.operators.postgres import PostgresOperator

path = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
sys.path.insert(0, path)

from modules.utils import get_titanic_dataset, pivot_dataset, mean_fare_per_class


# базовые аргументы DAG
args = {
    'owner': 'airflow',  # Информация о владельце DAG
    'start_date': dt.datetime(2020, 12, 23),  # Время начала выполнения пайплайна
    'retries': 1,  # Количество повторений в случае неудач
    'retry_delay': dt.timedelta(minutes=1),  # Пауза между повторами
    'depends_on_past': False,  # Запуск DAG зависит ли от успешности окончания предыдущего запуска по расписанию
}

# В контексте DAG'а зададим набор task'ок
with DAG(
        dag_id='my_super_titanic',  # Имя DAG
        schedule_interval=None,  # Периодичность запуска, например, "00 15 * * *"
        default_args=args,  # Базовые аргументы
) as dag:

    first_task = BashOperator(
        task_id='first_task',
        bash_command='echo "Here we start! Info: run_id={{ run_id }} | dag_run={{ dag_run }}"',
        dag=dag,
    )

    get_dataset = PythonOperator(
        task_id='get_titanic_dataset',
        python_callable=get_titanic_dataset,
        dag=dag,
    )

    create_pg_tables = PostgresOperator(
        task_id='create_table',
        sql='''
            CREATE TABLE IF NOT EXISTS {{ var.value.pg_table_pivot }}(                
                sex VARCHAR (8) NOT NULL,
                class01 integer NOT NULL, 
                class02 integer NOT NULL, 
                class03 integer NOT NULL
            );
            TRUNCATE TABLE {{ var.value.pg_table_pivot }};
            CREATE TABLE IF NOT EXISTS {{ var.value.pg_table_mean_fare_per_class }}(
                pclass integer NOT NULL, 
                fare numeric NOT NULL
            );    
            TRUNCATE TABLE {{ var.value.pg_table_mean_fare_per_class }};    
        ''',
        dag=dag,
    )

    mean_fares_titanic_dataset = PythonOperator(
        task_id='mean_fares_titanic_dataset',
        provide_context = True,
        python_callable=mean_fare_per_class,
        dag=dag,
    )

    pivot_titanic_dataset = PythonOperator(
        task_id='pivot_dataset',
        provide_context=True,
        python_callable=pivot_dataset,
        dag=dag,
    )

    last_task = BashOperator(
        task_id='last_task',
        bash_command='echo "Pipeline finished! Execution date is {{ ds }}"',
        dag=dag,
    )


    first_task >> get_dataset >> create_pg_tables >> [mean_fares_titanic_dataset, pivot_titanic_dataset] >> last_task