import pandas as pd
from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import Variable


pg_hook = PostgresHook(postgres_conn_id='postgres_default')


def get_titanic_dataset() -> dict:
    url = 'https://web.stanford.edu/class/archive/cs/cs109/cs109.1166/stuff/titanic.csv'
    df = pd.read_csv(url)
    return df.to_json()


def pivot_dataset(**kwargs):
    ti = kwargs['ti']
    titanic_json = ti.xcom_pull(key=None, task_ids='get_titanic_dataset')
    titanic_df = pd.read_json(titanic_json)
    result = titanic_df.pivot_table(
        index=['Sex'],
        columns=['Pclass'],
        values='Name',
        aggfunc='count'
    ).reset_index().to_dict(orient='records')
    pg_table_pivot = Variable.get("pg_table_pivot")
    pg_insert = f'insert into {pg_table_pivot} (sex, class01, class02, class03) values (%s, %s, %s, %s)'
    pg_hook.run(pg_insert, parameters=(result[0]['Sex'], result[0][1], result[0][2], result[0][3],))
    pg_hook.run(pg_insert, parameters=(result[1]['Sex'], result[1][1], result[1][2], result[1][3],))


def mean_fare_per_class(**kwargs):
    ti = kwargs['ti']
    titanic_json = ti.xcom_pull(key=None, task_ids='get_titanic_dataset')
    titanic_df = pd.read_json(titanic_json)
    result = titanic_df.groupby('Pclass')['Fare'].mean().reset_index().to_dict(orient='records')
    pg_table_mean_fare_per_class = Variable.get("pg_table_mean_fare_per_class")
    pg_insert = f'insert into {pg_table_mean_fare_per_class} (pclass, fare) values (%s, %s)'
    pg_hook.run(pg_insert, parameters=(result[0]['Pclass'], result[0]['Fare'],))
    pg_hook.run(pg_insert, parameters=(result[1]['Pclass'], result[1]['Fare'],))
    pg_hook.run(pg_insert, parameters=(result[2]['Pclass'], result[2]['Fare'],))
