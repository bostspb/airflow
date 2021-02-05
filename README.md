# GB: Настройка потоков данных. Apache Airflow
> **Geek University Data Engineering**

`Apache Airflow` `TaskFlow API` `crontab` `Jupyter Notebook` 

### Урок 1. Планирование задач. Введение Apache AirFlow

**Вопросы**
1. Какой из флагов утилиты crontab покажет список существующих кронов?
2. Напишите крон, который будет запускаться каждую пятницу в 9 часов вечера.
3. Напишите крон, который будет запускаться каждое воскресенье марта месяца 
на протяжении всего дня с интервалом в 4 часа 
(т.е. запуск будет в 2021-03-07 00:00:00, затем 2021-03-07 04:00:00 и т.д.)
4. Отметьте [все картинки](https://prnt.sc/wsjfr3), где изображен направленный ациклический граф.
5. Опишите своими словами, как Вы поняли, чем отличается `task` от `operator`?

[Ответы](https://github.com/bostspb/airflow/blob/main/lesson01/lesson01.md)

**Дополнительные материалы:**
* [Формат cron](http://www.nncron.ru/nncronlt/help/RU/working/cron-format.htm)
* [Проверка корректности cron'а](https://crontab.guru/)
* [Официальная документация Apache Airflow](https://airflow.apache.org/docs/apache-airflow/stable/index.html)
* [Концепции Apache Airflow](https://airflow.apache.org/docs/apache-airflow/stable/concepts.html)
* [Airflow Executors Explained](https://www.astronomer.io/guides/airflow-executors-explained/)
* [Airflow Tutorials on YouTube (на англ. языке)](https://www.youtube.com/watch?v=AHMm1wfGuHE&list=PLYizQ5FvN6pvIOcOd6dFZu3lQqc6zBGp2)


### Урок 2. Установка Airflow. Создание и основные параметры DAG

**Задание**
1. Установить и настроить Airflow по материалам лекции, создать проект в PyCharm, 
запустить пример DAG'а из лекции на локальном компьютере и убедиться в успешном расчете пайплайна.
2. Написать функцию `mean_fare_per_class()`, которая считывает файл `titanic.csv` и расчитывает среднюю 
арифметическую цену билета (Fare) для каждого класса (Pclass) и сохраняет результирующий датафрейм 
в файл `titanic_mean_fares.csv`
3. Добавить в DAG таск с названием `mean_fares_titanic_dataset`, 
который будет исполнять функцию mean_fare_per_class(), причем эта задача должна запускаться 
в параллель с `pivot_titanic_dataset` после таски `create_titanic_dataset`.
4. В конец пайплайна (после завершения тасок `pivot_titanic_dataset` и `mean_fares_titanic_dataset`) добавить шаг 
с названием `last_task`, на котором в STDOUT выводится строка, сообщающая об окончании расчета и выводящая 
execution date в формате YYYY-MM-DD. Пример строки: "Pipeline finished! Execution date is 2020-12-28"

**Формат сдачи д/з**: приложите ссылку на ваш Git с кодом DAG'а и туда же загрузите два скриншота с:
* выводом комманды в консоли "head ~/titanic_mean_fares.csv"
* содержанием лога инстанса таски last_task в UI

**Дополнительные материалы**
1. [PostgreSQL Client Applications](https://www.postgresql.org/docs/13/app-psql.html)
2. [PostgreSQL Server Applications](https://www.postgresql.org/docs/13/app-postgres.html)
3. [Введение в Apache Airflow](https://khashtamov.com/ru/apache-airflow-introduction/)
4. [Как мы оркестрируем процессы обработки данных с помощью Apache Airflow](https://habr.com/ru/company/lamoda/blog/518620/)
5. [Airflow — инструмент, чтобы удобно и быстро разрабатывать и поддерживать batch-процессы обработки данных](https://habr.com/ru/company/mailru/blog/339392/)

**Решение** <br>
[DAG](https://github.com/bostspb/airflow/blob/main/lesson02/second_dag.py) <br>
[Лог таски last_task в UI](https://github.com/bostspb/airflow/blob/main/lesson02/last_task_log.png) <br>
[Содержимое ~/titanic_mean_fares.csv](https://github.com/bostspb/airflow/blob/main/lesson02/result_csv_screenshot.png)


### Урок 3. Разработка потоков данных

**Задание** <br>
Реализовать новый вариант пайплайна:
1. Все функции вынесены в отдельный модуль и в **DAG** файле только сама структура графа (директория модулей должна быть в **PATH**)
2. Отказ от работы с локальными файлами:
    - сначала скачанный датасет пушится в **XCom** (он весит ~50 КБ)
    - затем он пуллится из **XCom** и передается двум преобразованиям (`pivot` и `mean_fare`)
3. Результаты преобразований записываются в две таблицы локальной базы PostgreSQL (**Connections+Hooks** или **psycopg2/sqlalchemy**).
4. Имена таблиц в **PostgreSQL** заданы в **Variables**

**Формат сдачи д/з** <br>
Приложите ссылку на ваш Git с кодом DAG'а и модулей, туда же загрузите скриншоты с:
* разделом Variables в UI с названиями таблиц;
* разделом XComs в UI с возвращенным значением исходного датасета;
* выводом консоли с select'ом топ-5 строк обеих таблиц в PostgreSQL (два результата расчета).

**Дополнительные материалы**
1. [Начало работы с Apache Airflow](https://www.machinelearningmastery.ru/getting-started-with-apache-airflow-df1aa77d7b1b/)
2. [Apache Airflow: делаем ETL проще](https://habr.com/ru/post/512386/)
3. [Integrating Slack alerts in Airflow](https://www.reply.com/data-reply/en/content/integrating-slack-alerts-in-airflow)
4. [Airflow XComs example](https://big-data-demystified.ninja/2020/04/15/airflow-xcoms-example-airflow-demystified/)
5. [Access the Airflow Database](https://www.astronomer.io/docs/cloud/stable/customize-airflow/access-airflow-database)
6. [Managing your Connections in Apache Airflow](https://www.astronomer.io/guides/connections)
7. [How to use PostgresOperator in Apache Airflow?](https://xnuinside.medium.com/short-guide-how-to-use-postgresoperator-in-apache-airflow-ca78d35fb435)
8. [ETL Pipelines With Airflow](http://michael-harmon.com/blog/AirflowETL.html) (пример с PostgreSQL)
9. [Building a Data Pipeline with Airflow](https://tech.marksblogg.com/airflow-postgres-redis-forex.html)

**Решение** <br>
[DAG](https://github.com/bostspb/airflow/blob/main/lesson03/dags/third_dag.py) <br>
[Module "utils"](https://github.com/bostspb/airflow/blob/main/lesson03/modules/utils.py) <br>
[Variables](https://github.com/bostspb/airflow/blob/main/lesson03/variables.png) <br>
[XComs](https://github.com/bostspb/airflow/blob/main/lesson03/xcoms.png) <br>
[Queries](https://github.com/bostspb/airflow/blob/main/lesson03/queries.png) <br>


### Урок 4. Airflow в production. Примеры реальных задач

**Задание** <br>
Перепишите пайплайн из предыдущего д/з с использованием новой фичи Airflow 2.0 - [TaskFlow API](https://airflow.apache.org/docs/apache-airflow/stable/tutorial_taskflow_api.html).

**Формат сдачи д/з** <br>
Приложите ссылку на ваш Git с кодом DAG'а.

**Дополнительные материалы**
1. [Airflow – платформа для разработки, планирования и мониторинга рабочих процессов](https://www.youtube.com/watch?v=A6YuWmwaTSw)
2. [Production Deployment](https://airflow.apache.org/docs/apache-airflow/stable/production-deployment.html)
3. [Best Practices](https://airflow.apache.org/docs/apache-airflow/stable/best-practices.html)
4. [Airflow FAQ](https://airflow.apache.org/docs/apache-airflow/stable/faq.html)
5. [7 достоинств и 5 недостатков Apache AirFlow](https://medium.com/@bigdataschool/7-достоинств-и-5-недостатков-apache-airflow-39fbbc80e702)
6. [Apache Airflow: автоматизация сбора ежедневных вложений электронной почты](https://www.machinelearningmastery.ru/apache-airflow-automating-the-collection-of-daily-email-attachments-213bc7128d3a/)
7. [Quick guide: How to run Apache Airflow with docker-compose](https://medium.com/@xnuinside/quick-guide-how-to-run-apache-airflow-cluster-in-docker-compose-615eb8abd67a)
8. [Airflow vs. Luigi: Which ETL Tool is the Best? ](https://www.xplenty.com/blog/airflow-vs-luigi/)
9. [Строим Data Pipeline на Python и Luigi](https://khashtamov.com/ru/data-pipeline-luigi-python/)
10. [How to Setup Airflow Multi-Node Cluster with Celery & RabbitMQ ](https://medium.com/@khatri_chetan/how-to-setup-airflow-multi-node-cluster-with-celery-rabbitmq-cfde7756bb6a)
11. [Обзор фреймворка Luigi для построения последовательностей выполнения задач ](https://habr.com/ru/company/otus/blog/339904/)
12. [Airflow vs. Luigi ](https://www.astronomer.io/guides/airflow-vs-luigi)
13. [AirFlow KubernetesExecutor: 3 способа запуска и 4 главных плюса для DevOps-инженера](https://medium.com/@bigdataschool/airflow-kubernetesexecutor-3-%D1%81%D0%BF%D0%BE%D1%81%D0%BE%D0%B1%D0%B0-%D0%B7%D0%B0%D0%BF%D1%83%D1%81%D0%BA%D0%B0-%D0%B8-4-%D0%B3%D0%BB%D0%B0%D0%B2%D0%BD%D1%8B%D1%85-%D0%BF%D0%BB%D1%8E%D1%81%D0%B0-%D0%B4%D0%BB%D1%8F-devops-%D0%B8%D0%BD%D0%B6%D0%B5%D0%BD%D0%B5%D1%80%D0%B0-cefd3acc833e)


**Решение** <br>
[DAG](https://github.com/bostspb/airflow/blob/main/lesson04/forth_dag.py)