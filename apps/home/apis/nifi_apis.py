from datetime import datetime, timedelta
import requests

from apps.home.Models.apps import *
from apps.home.Models.airflow import *
from apps.home.Models.etl_history import *
from apps.home.Models.recovery_history import *
from core.settings import \
    NIFI_ENDPOINT, \
    NIFI_PASSWORD, \
    NIFI_USERNAME
from django.views.generic import View
from django.http import JsonResponse


class NifiApis(View):

    NIFI_TOKEN = ''

    # generate every 1 hours
    NIFI_TOKEN_LIFETIME = ''

    @classmethod
    def get_nifi_headers(cls):

        if not cls.NIFI_TOKEN_LIFETIME:
            cls.NIFI_TOKEN_LIFETIME = datetime.now()
        
        if not cls.NIFI_TOKEN or cls.NIFI_TOKEN_LIFETIME + timedelta(minutes=1) <= datetime.now():
            head = \
            {
                'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                'Accept': '*/*',
            }

            data = \
            {
                'username': NIFI_USERNAME,
                'password': NIFI_PASSWORD
            }

            cls.NIFI_TOKEN = requests.post(NIFI_ENDPOINT + 'access/token', headers=head, data=data).text
        
            cls.NIFI_TOKEN_LIFETIME = datetime.now()
                
        headers = \
        {
            'Authorization': f'Bearer {cls.NIFI_TOKEN}',
            'Accept': 'application/json, text/javascript, */*; q=0.01',
        }

        return headers
    
    @classmethod
    def get_nifi_health_status(cls):

        headers = cls.get_nifi_headers()
        url = NIFI_ENDPOINT + 'flow/status'

        response = requests.get(url, headers=headers)
        response = response.json()

        return response


    @classmethod
    def get_nifi_status(cls):

        # about
        url = NIFI_ENDPOINT + 'flow/about'
        about_response = requests.get(url, headers=cls.get_nifi_headers())
        about_response = about_response.json()['about']

        # group
        url = NIFI_ENDPOINT + 'resources'
        group_response = requests.get(url, headers=cls.get_nifi_headers())
        group_response = group_response.json()['resources']

        process_list = []
        for item in group_response:
            if 'process-groups' in item['identifier']:
                process_id = item['identifier'].split('/')
                
                if len(process_id) != 3:
                    continue

                process_name = item['name']
                if process_name == 'NiFi Flow':
                    continue
                
                process_id = process_id[2]

                # group
                url = NIFI_ENDPOINT + 'process-groups/' + process_id
                processor_response = requests.get(url, headers=cls.get_nifi_headers())
                processor_response = processor_response.json()
                
                process = \
                {
                    'name': process_name,
                    'id': process_id,
                    'running': processor_response['runningCount'],
                    'stopped': processor_response['stoppedCount'],
                    'invalid': processor_response['invalidCount'],
                    'disabled': processor_response['disabledCount']
                }

                process_list.append(process)
        
        process_list.sort(key=lambda x: x['name'])
        
        identity = \
        {
            'version': about_response['version'],
            'timezone': about_response['timezone'],
            'buildTimestamp': about_response['buildTimestamp']
        }

        return NIFI_ENDPOINT.replace('-api',''), identity, process_list
    
    @classmethod
    def get_nifi_processors(cls, processor_id):
        # processor
        url = NIFI_ENDPOINT + 'process-groups/' + processor_id + '/processors'       
        processor_response = requests.get(url, headers=cls.get_nifi_headers())
        processor_response = processor_response.json()['processors']
        processors = []
        for item in processor_response:
            process = \
                {
                    'id': item['id'],
                    'name': item['status']['name'],
                    'status': item['status']['runStatus'],
                    'last': item['status']['statsLastRefreshed'],
                    'duration': item['status']['aggregateSnapshot']['tasksDuration'],
                    'version': item['revision']['version']
                }
            
            if item['revision'].get('clientId'):
                process['clientId'] =  item['revision']['clientId']

            processors.append(process)

        processors.sort(key=lambda x: x['name'])

        return processors
  
    @classmethod
    def get(cls, request):
        # get_nifi_processor_status
        processor_id = request.GET['id']
        
        processors = cls.get_nifi_processors(processor_id)
        
        return JsonResponse({
            'status' : 200,
            'processors' : processors
        })

    @classmethod
    def update_nifi_processor(cls, processorId, version, clientId, state):
        # processor
        url = NIFI_ENDPOINT + 'processors/' + processorId + '/run-status'
        data = {
            'revision': {
                'clientId': clientId,
                'version': version,
            },
            'state': state,
        }

        processor_response = requests.put(url, json = data, headers=cls.get_nifi_headers())

        return processor_response

    @classmethod
    def put(cls, request):
        # change processor status
        processorId = request.GET['processorId']
        version = request.GET['version']
        clientId = request.GET['clientId']
        state = request.GET['state']
        
        processor_response = cls.update_nifi_processor(processorId, version, clientId, state)
        
        if processor_response.ok:
            return JsonResponse({
                'status' : 200,
                'message': 'Update State Successful'
            })

        return JsonResponse({
            'status' : 400,
            'message': processor_response.text
        })

        # revision
        # id
        # uri
        # position
        # permissions
        # bulletins
        # component
        # inputRequirement
        # status
        # operatePermissions
