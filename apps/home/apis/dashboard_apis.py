from datetime import datetime, timedelta
from django.utils import timezone
from django.views.generic import View
from django.http import JsonResponse
import requests

from apps.home.apis.airflow_apis import AirflowApis
from apps.home.apis.validity_and_recovery_apis import ValidityAndRecoveryApis
from apps.home.apis.cdc_apis import CdcApis
from apps.home.apis.etl_apis import EtlAPis
from apps.home.apis.nifi_apis import NifiApis

from core.settings import \
    ETL_ENDPOINT, \
    ETL_ENDPOINT_AKUNTING

class DashboardApis(View):

    @classmethod
    def get(cls, request):
        
        cdc = cls.get_cdc_data()
        etl = cls.get_etl_data()
        nifi = cls.get_nifi_data()
        airflow_status, airflow = cls.get_airflow_data()
        recovery = cls.get_validity_and_recovery_data()
        health = cls.get_health_check_data(airflow_status)

        raw_time = datetime.now()
        time = str(raw_time.day) + '/' + str(raw_time.month) + '/' + str(raw_time.year) + ' ' + \
               str(raw_time.hour) + ':' + str(raw_time.minute) + ':' + str(raw_time.second)

        return JsonResponse({
            'airflow' : airflow,
            'etl' : etl,
            'cdc' : cdc,
            'nifi' : nifi,
            'health' : health,
            'time' : time,
            'recovery' : recovery,
            'raw_time' : raw_time,
            'status' : 200
        })
    
    @classmethod
    def get_health_check_data(cls, airflow_status):
        # obtain health check data
        summary = {
            'airflow' : 'Unhealthy',
            'etl' : 'Unhealthy',
            'etl_akunting' : 'Unhealthy',
            'datamart_mysql' : 'Unhealthy',
            'datamart_postgres' : 'Unhealthy',
            'nifi' : 'Unhealthy',
            'ok_total' :0,
            'unhealthy_total': 5
        }

        # airflow
        try:
            if 'healthy' in airflow_status['metadatabase_status'].lower() and \
                'healthy' in airflow_status['scheduler_status'].lower():
                summary['airflow'] = 'OK'
                summary['ok_total'] += 1
                summary['unhealthy_total'] -= 1
        except:
            pass

        # etl
        try:
            url = ETL_ENDPOINT + 'health'

            response = requests.get(url)
            response = response.json()['status']

            if 'success' in response.lower():
                summary['etl'] = 'OK'
                summary['ok_total'] += 1
                summary['unhealthy_total'] -= 1
        except:
            pass

        # etl akunting
        try:
            url = ETL_ENDPOINT_AKUNTING + 'health'

            response = requests.get(url)
            response = response.json()['status']

            if 'success' in response.lower():
                summary['etl_akunting'] = 'OK'
                summary['ok_total'] += 1
                summary['unhealthy_total'] -= 1
        except:
            pass
        
        # nifi
        try:
            response = NifiApis.get_nifi_health_status()
            summary['nifi'] = 'OK'
            summary['ok_total'] += 1
            summary['unhealthy_total'] -= 1
        except:
            pass

        # datamart postgres
        try:
            RawDatamartAddonHistory.objects.using('datamart_postgres').last()
            summary['datamart_postgres'] = 'OK'
            summary['ok_total'] += 1
            summary['unhealthy_total'] -= 1
        except:
            pass

        return summary
        
    @classmethod
    def get_etl_data(cls):
        # obtain etl data
        summary = {
            'etl_plugged' : 0,
            'datamart_updated' : 0,
            'datamart_outdated' : 0,
            'execution' : 0,
            'no_execution' : 0
        }

        try:
            etl, etl_postgres = EtlAPis.get_elt_histories()
            action_threshold = (timezone.localtime() - timedelta(hours=2)).replace(tzinfo=None)
            datamart_threshold = (timezone.localtime() - timedelta(days=1)).replace(tzinfo=None)

            for _, item in etl.items():
                summary['etl_plugged'] += 1

                if (item.actdate).replace(tzinfo=None) < action_threshold:
                    summary['no_execution'] += 1
                else:
                    summary['execution'] += 1
                
                if (item.ts_end).replace(tzinfo=None) < datamart_threshold:
                    summary['datamart_outdated'] += 1
                else:
                    summary['datamart_updated'] += 1

            for _, item in etl_postgres.items():
                summary['etl_plugged'] += 1

                if (item.actdate).replace(tzinfo=None) < action_threshold:
                    summary['no_execution'] += 1
                else:
                    summary['execution'] += 1
                
                if (item.ts_end).replace(tzinfo=None) < datamart_threshold:
                    summary['datamart_outdated'] += 1
                else:
                    summary['datamart_updated'] += 1

        except:
            pass

        return summary

    @classmethod
    def get_cdc_data(cls):
        # obtain cdc data
        summary = {
            'connectors_plugged' : 0,
            'running_connectors' : 0,
            'running_tasks' : 0,
            'connectors_failed' : 0,
            'tasks_failed' : 0,
        }

        try:
            _, connectors = CdcApis.get_cdc_status()
            for item in connectors:
                summary['connectors_plugged'] += 1

                if item['connector_status'] == 'RUNNING':
                    summary['running_connectors'] += 1
                else:
                    summary['connectors_failed'] += 1

                if item['task_status'] == 'RUNNING':
                    summary['running_tasks'] += 1
                else:
                    summary['tasks_failed'] += 1
            
            return summary
        except:
            pass

    @classmethod
    def get_nifi_data(cls):
        # obtain nifi data
        summary = {
            'processor_groups_plugged' : 0,
            'running_processors' : 0,
            'processors_stopped' : 0,
            'processors_disabled' : 0,
            'processors_invalid' : 0
        }

        try:
            _,_, processors = NifiApis.get_nifi_status()
            for item in processors:
                summary['processor_groups_plugged'] += 1
                summary['running_processors'] += item['running']
                summary['processors_stopped'] += item['stopped']
                summary['processors_invalid'] += item['invalid']
                summary['processors_disabled'] += item['disabled']
        except:
            pass

        return summary
    
    @classmethod
    def get_airflow_data(cls):
        # obtain airflow data
        summary = {
            'dags_plugged' : 0,
            'running_dags' : 0,
            'dags_paused' : 0,
            'task_failed' : 0,
            'general_error' : 0
        }

        identity = None

        try:
            identity, dag_list, general_error, failed_task = AirflowApis.get_airflow_status()
            error_threshold = (timezone.localtime() - timedelta(days=2)).replace(tzinfo=None)

            summary['general_error'] = len(general_error)


            for item in failed_task:
                if (item['last_failed_at']).replace(tzinfo=None) > error_threshold:
                    summary['task_failed'] += 1

            for item in dag_list:
                summary['dags_plugged'] += 1
                if item['is_paused']:
                    summary['dags_paused'] += 1
                else:
                    summary['running_dags'] += 1
        except:
            pass

        return identity, summary
    
    @classmethod
    def get_validity_and_recovery_data(cls):
        # obtain validity and recovery data
        summary = {
            'recovery_plugged' : 0,
            'validity_plugged' : 0,
            'recovered' : 0,
            'wait_to_recover' : 0,
            'no_validation' : 0
        }

        try:
            validities, recoveries, _, _, schedulers = ValidityAndRecoveryApis.get_histories()
            error_threshold = (timezone.localtime() - timedelta(days=2)).replace(tzinfo=None)

            summary['recovery_plugged'] = len(recoveries)

            for _, item in validities.items():
                summary['validity_plugged'] += 1

                if (item['actdate']).replace(tzinfo=None) < error_threshold:
                    summary['no_validation'] += 1

                if item['is_waiting'] > 0:
                    summary['wait_to_recover'] += 1
                else:
                    summary['recovered'] += 1

        except:
            pass
    
        return summary
