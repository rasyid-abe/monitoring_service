import psycopg2
from datetime import timedelta
from django.utils import timezone
import requests
from concurrent.futures import ThreadPoolExecutor
from apps.home.Models.etl_history import ETLList
from django.db import connection
from core.settings import DATABASES

datalake_cred = DATABASES['datamart_postgres']
db_name = datalake_cred['NAME']
username = datalake_cred['USER']
password = datalake_cred['PASSWORD']
host = datalake_cred['HOST']
port = datalake_cred['PORT']

def get_active_apis(is_reset=False):
    conn = psycopg2.connect(database=db_name, user=username, password=password, host=host, port=port)
    cursor = conn.cursor()

    sql_query = \
    """
    SELECT
        id, 
        endpoint, 
        is_running,
        updated_at
    FROM 
        mart_prd.etl_list
    """
    if not is_reset:
        sql_query += " WHERE is_active = true"
        
    cursor.execute(sql_query)
    active_apis = cursor.fetchall()
    conn.close()

    return active_apis

def update_state(etl_id, state):
    query = \
    f"""
    UPDATE 
        mart_prd.etl_list set 
        is_running = {state}, 
        updated_at = '{(timezone.localtime()).replace(tzinfo=None)}'
    WHERE 
        id = {etl_id}
    """

    conn = psycopg2.connect(database=db_name, user=username, password=password, host=host, port=port)
    mycursor = conn.cursor()
    mycursor.execute(query)
    conn.commit()
    conn.close()

def reset_state():
    etl_list = get_active_apis(True)

    for etl_record in etl_list:
        update_state(etl_record[0], False)

def execute_api(etl_id, endpoint, is_running, updated_at, threshold_time):
    if is_running:

        if updated_at <= threshold_time:
            update_state(etl_id, False)

        return 0

    try:
        update_state(etl_id, True)
        x = requests.get(endpoint)
    except:
        pass

    update_state(etl_id, False)

def start():
    etl_list = get_active_apis()

    threshold_time = (timezone.localtime() - timedelta(hours=2)).replace(tzinfo=None)
    executor = ThreadPoolExecutor()
    for etl_record in etl_list:

        executor.submit(execute_api, etl_record[0], etl_record[1],
                        etl_record[2], etl_record[3], threshold_time)

