from django.db.models import Max, Count
import base64
import requests
import json
from datetime import datetime, timedelta

from apps.home.Models.airflow import *
from apps.home.Models.apps import *
from apps.home.Models.etl_history import *
from apps.home.Models.recovery_history import *
from core.settings import \
    AIRFLOW_ENDPOINT, \
    AIRFLOW_PASSWORD, \
    AIRFLOW_USERNAME
from django.views.generic import View
from django.http import JsonResponse

class AirflowApis(View):

    AIRFLOW_HEADER = ''

    @classmethod
    def get_airflow_request_headers(cls):

        if not cls.AIRFLOW_HEADER:
            credential = base64.b64encode((AIRFLOW_USERNAME + ':' + AIRFLOW_PASSWORD).encode("ascii")).decode('UTF-8')
            credential = 'Basic ' + credential

            AIRFLOW_HEADER = {
                "Content-Type": "application/json; charset=utf-8",
                "Authorization": credential
            }
        
        return AIRFLOW_HEADER

    @classmethod
    def get_airflow_status(cls):
        # about
        url = AIRFLOW_ENDPOINT + 'health'
        response = requests.get(url, headers=cls.get_airflow_request_headers())
        response = response.json()

        identity = \
        {
          'latest_scheduler_heartbeat' : cls.time_conversion(response['scheduler']['latest_scheduler_heartbeat']),
          'metadatabase_status' : response['metadatabase']['status'],
          'scheduler_status' : response['scheduler']['status'],
        }

        url = AIRFLOW_ENDPOINT + 'version'
        response = requests.get(url, headers=cls.get_airflow_request_headers())
        response = response.json()

        identity['version'] = response['version'] 

        # Dags
        url = AIRFLOW_ENDPOINT + 'dags'
        response = requests.get(url, headers=cls.get_airflow_request_headers())
        response = response.json()

        dag_list = []

        for item in response['dags']:

            last_execution = cls.time_conversion(item['last_parsed_time'], 0)
            latest_data = item['next_dagrun_data_interval_start']

            latest_data = cls.time_conversion(latest_data, 1)
            dag = \
            {
                'name' : item['dag_id'],
                'is_paused' : item['is_paused'],
                'last_execution' : last_execution,
                'schedule_interval' : item['timetable_description'],
                'latest_data' : latest_data
            }

            dag_list.append(dag)

        dag_list.sort(key=lambda x: x['name'])

        # get general error
        general_error = AirflowGeneralError.objects.using('airflow') \
            .order_by('filename') \
            .all()

        # get failed task
        failed_task = AirflowFailedTask.objects.using('airflow') \
            .values('dag_id', 'task_id') \
            .order_by('dag_id', 'task_id') \
            .annotate(last_failed_at=Max('end_date'), failed_total=Count('pk'))

        return identity, dag_list, general_error, failed_task
    
    @classmethod
    def time_conversion(cls, time, type=0):
        if not time:
            return ''

        if type == 0:
            time = datetime.strptime(time, '%Y-%m-%dT%H:%M:%S.%f%z')
        else:
            time = datetime.strptime(time, '%Y-%m-%dT%H:%M:%S%z')
        
        time = time + timedelta(hours=7)
        time = str(time)

        result = time.split(' ')
        date = result[0].split('-')
        date = date[2] + '/' + date[1] + '/' + date[0]
        time = ''

        if type == 0:
            time = result[1].split('.')[0]
        else:
            time = result[1].split('+')[0]

        result = date + ' ' + time

        return result
        
    @classmethod
    def run_dag(cls, id, state):
        url = AIRFLOW_ENDPOINT + 'dags/' + id

        if state == 'False':
            state = False
        else:
            state = True

        body = json.dumps({"is_paused" : state})

        response = requests.patch(url, headers=cls.get_airflow_request_headers(), data=body)
        response = response.json()

        return response
    
    @classmethod
    def get(cls, request):
        
        if not request.GET.get('type'):
            # get dag tasks
            dag_id = request.GET['id']
            
            # tasks
            url = AIRFLOW_ENDPOINT + 'dags/' + dag_id + '/tasks'
            response = requests.get(url, headers=cls.get_airflow_request_headers())
            response = response.json()

            tasks = []
            for item in response['tasks']:
                task = \
                {
                    'name': item['task_id'],
                    'start_date': cls.time_conversion(item['start_date'], 1),
                    'end_date': cls.time_conversion(item['end_date'], 1),
                }

                tasks.append(task)

            return JsonResponse({
                'status' : 200,
                'taks' : tasks
            })
        else:
            _, dag_list, _, _ = cls.get_airflow_status()

            return JsonResponse({
                'status' : 200,
                'data' : dag_list
            })

    @classmethod
    def put(cls, request):
        dag_id = request.GET['id']
        purpose =  request.GET['purpose']
        response = ''

        if purpose == 'run_dag':
            state = request.GET['state']
            response = cls.run_dag(dag_id, state)
        
        return JsonResponse({
            'response' : response,
            'status': 200
        })


        
    