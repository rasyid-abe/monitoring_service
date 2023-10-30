from apps.home.Models.apps import *
from apps.home.Models.airflow import *
from apps.home.Models.etl_history import *
from apps.home.Models.recovery_history import *
import requests
from core.settings import \
    NIFI_ENDPOINT, \
    NIFI_PASSWORD, \
    NIFI_USERNAME
from django.utils import timezone
from datetime import timedelta, datetime
import json
import uuid


class NifiJobs:

    NIFI_TOKEN = ''

    # generate every 1 hours
    NIFI_TOKEN_LIFETIME = ''


    @classmethod
    def nifi_restart(cls):

            status = cls.get_nifi_status()

            process_group = {
                'ETL MART SalesAddonDetail Seq5Min - Postgres': RawDatamartAddonDetailHistory,
                'ETL MART SalesAddon Seq5Min - Postgres': RawDatamartAddonHistory,
                'ETL MART BusiestItemTime Seq5Min - Postgres': RawDatamartBusiestItemTimeHistory,
                'ETL MART Cashier Seq5Min - Postgres': RawDatamartCashierHistory,
                'ETL MART Sales Promo-Kupon-Poin Seq45Min - Postgres': RawDatamartPromoHistory,
                'ETL MART Reservation Seq5Min - Postgres': RawDatamartReservationHistory,
                'ETL MART Utilization Seq45Min - Postgres': RawDatamartUtilizationHistory,
                'ETL MART Compliment Seq5Min - Postgres': RawDatamartComplimentHistory,
                'ETL MART Dashboard Seq5Min - Pandas': RawDatamartSalesDashboardHistory
            }

            for key, data in process_group.items():
                pg_id = ''
                for r in status['resource']['resources']:
                    if r['name'] == key:
                        raw_id = r['identifier'].split('/')
                        pg_id = raw_id[-1]

                last_act = data.objects.using('datamart_postgres').values().last()['actdate']
                if isinstance(last_act, datetime):
                    last_time = last_act.replace(tzinfo=None)
                else:
                    last_time = datetime.strptime(last_act, '%Y-%m-%d %H:%M:%S %z').replace(tzinfo=None)

                execution_threshold = (timezone.localtime() - timedelta(hours=2)).replace(tzinfo=None)

                if last_time < execution_threshold:
                    print(key + 'start')
                    cls.change_pg_state(status['headers'], pg_id, 'RUNNING')

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
    def get_nifi_status(cls):
        client_id = uuid.uuid4()

        url = NIFI_ENDPOINT + 'resources'
        group_response = requests.get(url, headers=cls.get_nifi_headers())

        pg_name = 'NiFi Flow'

        root_pg_id = ''
        resource = json.loads(group_response.text)
        for x in resource['resources']:
            if ((x['name'] == pg_name) and ("/process-groups/" in x['identifier'])):
                pgid = x['identifier'].split('/')
                root_pg_id = pgid[-1]

        params = {
            'client_id' : client_id,
            'root_pg_id' : root_pg_id,
        }

        return  {
            'resource': resource,
            'params': params,
            'headers': cls.get_nifi_headers(),
        }

    @classmethod
    def get_process_group(cls, params, headers, pg_name):
        obj = \
        {
            "revision":{
                "clientId":str(params['client_id']),
                "version":0
            },
            "component":{
                "name":pg_name,
            }
        }

        url = f"{NIFI_ENDPOINT}process-groups/{str(params['root_pg_id'])}/process-groups"
        act = requests.post(url, json = obj, headers=headers)
        json_pg = json.loads(act.text)
        return json_pg['id']

    @classmethod
    def change_pg_state(cls, headers, proc_id, state):
        obj = {"id":str(proc_id),"state":state}
        url = f"{NIFI_ENDPOINT}flow/process-groups/{proc_id}"
        act = requests.put(url, json = obj, headers=headers)
