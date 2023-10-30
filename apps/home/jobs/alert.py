from apps.home.Models.apps import Alert, \
    AlertDetail, \
    AlertHistory
from apps.home.apis.etl_apis import EtlAPis
from apps.home.apis.dashboard_apis import DashboardApis
from apps.home.apis.cdc_apis import CdcApis
from apps.home.apis.alert_apis import AlertApis
from django.utils import timezone
from datetime import timedelta
from json import dumps
from httplib2 import Http

class AlertJobs:

    @classmethod
    def alert_check(cls):
        # checking etl

        try:
            etl_error = cls.etl_check()
            cls.store_error_log(etl_error)
            cls.push_notification(etl_error)
        except:
            pass

        try:
            # checking health check 
            health_check_error = cls.health_check()
            cls.store_error_log(health_check_error)
            cls.push_notification(health_check_error)
        except:
            pass

        try:
            # checking health check 
            cdc_check_error = cls.cdc_check()
            cls.store_error_log(cdc_check_error)
            cls.push_notification(cdc_check_error)
        except:
            pass

    @classmethod
    def cdc_check(cls):

        alert = Alert.objects.get(id=3)
        if not alert.status:
            print(f'[Alert] checking Skipped : {alert.alert_name}')
            return []

        print(f'[Alert] checking : {alert.alert_name}')

        _, cdc_list = CdcApis.get_cdc_status()
        cdc_alert = AlertDetail.objects \
            .filter(id_alert_id = 3) \
            .get()
        
        errors = []
        for item in cdc_list:
            if item['task_status'] == 'FAILED':
                errors.append({
                    'message' : f'See error details on De Dashboard or Kafka',
                    'type' : 2,
                    'id_detail' : cdc_alert.id,
                    'id_alert' : 3,
                    'alert_name' : alert.alert_name,
                    'alert_detail_name' : item['name'],
                })
        
        return errors

    @classmethod
    def etl_check(cls):

        alert = Alert.objects.get(id=1)
        if not alert.status:
            print(f'[Alert] checking Skipped : {alert.alert_name}')
            return []

        # get ETL histories
        etl_histories = EtlAPis.get_elt_histories()
        etl_alert = AlertDetail.objects \
            .filter(id_alert_id = 1) \
            .order_by('alert_detail_name') \
            .all()
        
        errors = []

        thresholds = AlertApis.get_configurations()
        execution_threshold = (timezone.localtime() - timedelta(minutes=thresholds[1].value['threshold_in_minute'])).replace(tzinfo=None)
        data_threshold = (timezone.localtime() - timedelta(minutes=thresholds[0].value['threshold_in_minute'])).replace(tzinfo=None)
        for item in etl_alert:
            if not item.status:
                continue

            try:
                etl = etl_histories[item.alert_detail_name]
            except:
                continue

            if '0' in str(item.detail):
                if (etl.actdate).replace(tzinfo=None) < execution_threshold:
                    errors.append({
                        'message' : f'No Execution More Than {thresholds[1].value["threshold_in_minute"]} Minutes! Last Executed at : {etl.actdate.replace(tzinfo=None)}',
                        'type' : 2,
                        'id_detail' : item.id,
                        'id_alert' : 1,
                        'alert_name' : alert.alert_name,
                        'alert_detail_name' : item.alert_detail_name
                    })
            else:
                if (etl.ts_end).replace(tzinfo=None) < data_threshold:
                    errors.append({
                        'message' : f'Data is Oudated. More Than {thresholds[0].value["threshold_in_minute"]} Minutes! Latest Data is : {etl.ts_end.replace(tzinfo=None)}',
                        'type' : 1,
                        'id_detail' : item.id,
                        'id_alert' : 1,
                        'alert_name' : alert.alert_name,
                        'alert_detail_name' : item.alert_detail_name,
                    })

        return errors
    
    @classmethod
    def health_check(cls):

        alert = Alert.objects.get(id=2)
        if not alert.status:
            print(f'[Alert] checking Skipped : {alert.alert_name}')
            return []

        print(f'[Alert] checking : {alert.alert_name}')
        
        airflow_status, _ = DashboardApis.get_airflow_data()
        services = DashboardApis.get_health_check_data(airflow_status)
        health_check_alert = AlertDetail.objects \
            .filter(id_alert_id = 2) \
            .order_by('alert_detail_name') \
            .all()

        map_name = \
        {
            'Airflow' : 'airflow',
            'ETL Spark' : 'etl',
            'ETL Akunting Spark' : 'etl_akunting',
            'Datamart Database (Mysql)' : 'datamart_mysql',
            'Datamart Database (Postgres)' : 'datamart_postgres',
            'NIFI' : 'nifi',
        }

        errors = []
        for item in health_check_alert:
            if not item.status:
                continue

            health_check = services[map_name[item.alert_detail_name]]

            if health_check != 'OK':
                errors.append({
                    'message' : f'Service is Unhealthy!',
                    'type' : 2,
                    'id_detail' : item.id,
                    'id_alert' : 2,
                    'alert_name' : alert.alert_name,
                    'alert_detail_name' : item.alert_detail_name,
                })
        
        return errors

    @classmethod
    def store_error_log(cls, errors):
        for item in errors:
            object = AlertHistory(
                id_alert_detail_id = item['id_detail'],
                type = item['type'],
                message = item['message'],
                created_at = (timezone.localtime() + timedelta(hours=7)).replace(tzinfo=None)
            )

            object.save()
    
    @classmethod
    def push_notification(cls, errors):
        # space - live (de alert)
        url = 'https://chat.googleapis.com/v1/spaces/AAAAO8_pRWI/messages?key=AIzaSyDdI0hCZtE6vySjMm-WEfRq3CPzqKqqsHI&token=lpTUCNYSgWT_PuswF-R6GXqLzgSfQkmBItkW7Jkk4Kc%3D'
        
        # space - live (service-alert-charlie)
        url_2 = 'https://chat.googleapis.com/v1/spaces/AAAAlmC1qMo/messages?key=AIzaSyDdI0hCZtE6vySjMm-WEfRq3CPzqKqqsHI&token=_RNHRhzJPlgyhWPdNCd4vP1LyBVbKuaZJgqXeEi6Xb4%3D'

        # space - testing
        # url = 'https://chat.googleapis.com/v1/spaces/AAAAJlaLdfc/messages?key=AIzaSyDdI0hCZtE6vySjMm-WEfRq3CPzqKqqsHI&token=icsth9LJGIi9jQPrp5UCdAqw2pByc12XVqv_ySGL69k%3D'

        for error in errors:
            message = f'[{error["alert_name"]} -]'
            if error['alert_detail_name']:
                message = message.replace('-', f'- {error["alert_detail_name"]}')
            else:
                message = message.replace('-', '')

            message += f' {error["message"]}'
            bot_message = {'text' : message}
            message_headers = {'Content-Type': 'application/json; charset=UTF-8'}
            http_obj = Http()
            
            response_1 = http_obj.request(
                uri=url,
                method='POST',
                headers=message_headers,
                body=dumps(bot_message),
            )
            
            if error['id_alert'] == 1:
                response_2 = http_obj.request(
                    uri=url_2,
                    method='POST',
                    headers=message_headers,
                    body=dumps(bot_message),
                )
