import requests
from datetime import timedelta

from apps.home.Models.apps import *
from apps.home.Models.airflow import *
from apps.home.Models.etl_history import *
from apps.home.Models.recovery_history import *
from django.http import JsonResponse, HttpResponseRedirect
from core.settings import KAFKA_ENDPOINT
from django.views.generic import View

class CdcApis(View):

    @classmethod
    def get_cdc_status(cls):

        # about
        url = KAFKA_ENDPOINT
        about_response = requests.get(url)
        about_response = about_response.json()

        # connectors
        url = KAFKA_ENDPOINT + 'connectors?expand=status'
        connectors_response = requests.get(url)
        connectors_response = connectors_response.json()

        connector_list = []
        for item, status in connectors_response.items():
            name = item.replace('debezium-', '')
            name = name.replace('debezium.', '')
            tmp = {
                'name': name,
                'connector_status': status['status']['connector']['state'],
                'task_status': status['status']['tasks'][0]['state'],
                'task_trace' : '',
                'restart_url': KAFKA_ENDPOINT + 'connectors/' + item + '/tasks/0/restart',
                'n_task'     : len(status['status']['tasks'])
            }
            
            if tmp['task_status'] == 'FAILED':
                tmp['task_trace'] = status['status']['tasks'][0]['trace']

            connector_list.append(tmp)
        
        connector_list.sort(key=lambda x: x['name'])

        identity = \
        {
            'version': about_response['version'],
            'commit': about_response['commit'],
            'cluster_id': about_response['kafka_cluster_id']
        }

        return identity, connector_list
    
    @classmethod
    def get_cdc_data(cls):

        cdc_histories = ValidityHistoryCDC.objects.using('datamart_postgres') \
            .order_by('table_name', '-id') \
            .distinct('table_name') \
            .values()[:500]

        dispute_table_count = 0

        for item in cdc_histories:
            dispute = abs(item['data_source'] - item['data_target'])
            item['actdate'] += timedelta(hours=7) 
            item['dispute'] = dispute
            
            if dispute >= 100:
                dispute_table_count += 1 


        return dispute_table_count, cdc_histories
    
    @classmethod
    def get(cls, request):

        table_name = request.GET['table_name']
        cdc_data_histories = ValidityHistoryCDC.objects.using('datamart_postgres') \
            .filter(table_name = table_name) \
            .order_by('-id') \
            .values()[:100]
        
        for item in cdc_data_histories:
            item['dispute'] = abs(item['data_source'] - item['data_target'])
            item['data_source'] = f'{int(item["data_source"]):,}'
            item['data_target'] = f'{int(item["data_target"]):,}'
            item['dispute'] = f'{int(item["dispute"]):,}'
            item['execution_time'] = '{:>12,.2f}'.format(item['execution_time'] / 60)
            
        data = list(cdc_data_histories)

        return JsonResponse({
                'status' : 200,
                'data': data
            })
    
    @classmethod
    def restart(cls, request):

        data = request.POST.dict()
        restart_url = data.get('restart-url')
        n_task = int(data.get('n-task'))

        # task number 0
        response = requests.post(restart_url)

        # task number > 0
        if n_task > 1:
            for i in range(1, n_task):
                restart_url_i = restart_url.replace('/0/', f'/{i}/')
                response = requests.post(restart_url_i)

        return HttpResponseRedirect('/cdc-status.html')
