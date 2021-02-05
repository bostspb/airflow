import datetime as dt
import pandas as pd
from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import Variable
from airflow.decorators import dag, task


# базовые аргументы DAG
args = {
    'owner': 'airflow',  # Информация о владельце DAG
    'start_date': dt.datetime(2020, 12, 23),  # Время начала выполнения пайплайна
    'retries': 1,  # Количество повторений в случае неудач
    'retry_delay': dt.timedelta(minutes=1),  # Пауза между повторами
    'depends_on_past': False,  # Запуск DAG зависит ли от успешности окончания предыдущего запуска по расписанию
}

@dag(default_args=args, schedule_interval=None, dag_id='my_super_titanic_v2')
def titanic_pipeline_taskflow():
    @task()
    def first_task():
        print('Here we start! Info: run_id={{ run_id }} | dag_run={{ dag_run }}')
        return True

    @task()
    def create_pg_tables(*args):
        pg_hook = PostgresHook()
        sql = f'''
            CREATE TABLE IF NOT EXISTS {Variable.get("pg_table_pivot")}(                
                sex VARCHAR (8) NOT NULL,
                class01 integer NOT NULL, 
                class02 integer NOT NULL, 
                class03 integer NOT NULL
            );
            TRUNCATE TABLE {Variable.get("pg_table_pivot")};
            CREATE TABLE IF NOT EXISTS {Variable.get("pg_table_mean_fare_per_class")}(
                pclass integer NOT NULL, 
                fare numeric NOT NULL
            );    
            TRUNCATE TABLE {Variable.get("pg_table_mean_fare_per_class")};    
        ''',
        pg_hook.run(sql)

    @task()
    def get_titanic_dataset(*args) -> dict:
        url = 'https://web.stanford.edu/class/archive/cs/cs109/cs109.1166/stuff/titanic.csv'
        df = pd.read_csv(url)
        return df.to_json()

    @task()
    def pivot_dataset(titanic_json:dict) -> dict:
        return pd.read_json(titanic_json).pivot_table(
            index=['Sex'],
            columns=['Pclass'],
            values='Name',
            aggfunc='count'
        ).reset_index().to_dict(orient='records')

    @task()
    def set_to_pg_table_pivot(data: dict):
        pg_hook = PostgresHook()
        pg_insert = f'insert into {Variable.get("pg_table_pivot")} (sex, class01, class02, class03) values (%s, %s, %s, %s)'
        for row in data:
            pg_hook.run(pg_insert, parameters=(row['Sex'], row[1], row[2], row[3],))
        return True

    @task()
    def mean_fare_per_class(titanic_json: dict) -> dict:
        return pd.read_json(titanic_json)\
            .groupby('Pclass')['Fare']\
            .mean().reset_index()\
            .to_dict(orient='records')

    @task()
    def set_to_pg_table_mean_fare_per_class(data: dict):
        pg_hook = PostgresHook()
        pg_insert = f'insert into {Variable.get("pg_table_mean_fare_per_class")} (pclass, fare) values (%s, %s)'
        for row in data:
            pg_hook.run(pg_insert, parameters=(row['Pclass'], row['Fare'],))
        return True

    @task()
    def last_task(*args):
        print('Pipeline finished! Execution date is {{ ds }}')
        return True

    start = first_task()
    prepare = create_pg_tables(start)

    titanic_json = get_titanic_dataset(prepare)

    pivot_json = pivot_dataset(titanic_json)
    db_result_1 = set_to_pg_table_pivot(pivot_json)

    mean_fare_per_class_json = mean_fare_per_class(titanic_json)
    db_result_2 = set_to_pg_table_mean_fare_per_class(mean_fare_per_class_json)

    last_task(db_result_1, db_result_2)

start_pipeline = titanic_pipeline_taskflow()