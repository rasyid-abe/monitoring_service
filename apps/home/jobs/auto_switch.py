from apps.home.Models.etl_history import DashboardReportStatus
from apps.home.Models.apps import Alert, \
    AlertDetail, \
    AlertHistory
from apps.home.apis.etl_status_apis import EtlStatusAPis
from django.utils import timezone
from apps.home.Models.klopos import *
from datetime import timedelta
from json import dumps
from django.apps import apps
from httplib2 import Http

class AutoSwitchJobs:

    @classmethod
    def check(cls):
        
        report_list = cls.get_mapping_table_data()
        model_list = cls.get_all_models()
        data_threshold = (timezone.localtime() - timedelta(hours=2)).replace(tzinfo=None)
        data_threshold_back = (timezone.localtime() - timedelta(minutes=30)).replace(tzinfo=None)

        for report in report_list:

            if not report['is_automate']:
                continue

            print(f'checking : {report["report_name"]}')

            latest_data = cls.get_latest_data(model_list[report['history_table_name']])

            # delay more than threshold
            # get current status : datamart or non-datamart
            report_status = cls.get_report_status(report)
            
            if latest_data < data_threshold:
                # switch datamart into non-datamart
                if report_status:
                    EtlStatusAPis.switch_datamart(report['id_m_cms_menu'], 'False')
                    print(f'{report["report_name"]} - switched to non-datamart')
                    cls.push_notification(report, latest_data, report_status)
            else:
                # switch again into datamart if reach the threshold
                if latest_data >= data_threshold_back:
                    if not report_status:
                        EtlStatusAPis.switch_datamart(report['id_m_cms_menu'], 'True')
                        print(f'{report["report_name"]} - switched to datamart')
                        cls.push_notification(report, latest_data, report_status)

    @classmethod
    def get_report_status(cls, report):
        """
        True = datamart
        False = non-datamart
        """
        status = False

        cockpit_token = EtlStatusAPis.get_cockpit_token()
        menu = EtlStatusAPis.get_cockpit_menu(cockpit_token, report['id_m_cms_menu'])

        if report['datamart_url'] in menu['content']:
            status = True

        return status

    @classmethod
    def get_latest_data(cls, table_name):

        model = apps.get_model('home', table_name)
        latest_data = model.objects \
            .using('datamart_postgres') \
            .order_by('ts_end') \
            .last()
        
        return (latest_data.ts_end + timedelta(hours=7)).replace(tzinfo=None)

    @classmethod
    def get_all_models(cls):
        all_models = apps.get_models()
        history_map = {}
        for item in all_models:
            if 'raw' in item._meta.db_table:
                history_map[item._meta.db_table] = item.__name__
        
        return history_map

    @classmethod
    def get_mapping_table_data(cls):

        report_list = DashboardReportStatus.objects \
            .using('datamart_postgres') \
            .order_by('report_name') \
            .values()
        
        return report_list

    @classmethod
    def push_notification(cls, report, latest_data, status):
        # space - live (de alert)
        url = 'https://chat.googleapis.com/v1/spaces/AAAAO8_pRWI/messages?key=AIzaSyDdI0hCZtE6vySjMm-WEfRq3CPzqKqqsHI&token=lpTUCNYSgWT_PuswF-R6GXqLzgSfQkmBItkW7Jkk4Kc%3D'
        
        # space - live (service-alert-charlie)
        url_2 = 'https://chat.googleapis.com/v1/spaces/AAAAlmC1qMo/messages?key=AIzaSyDdI0hCZtE6vySjMm-WEfRq3CPzqKqqsHI&token=_RNHRhzJPlgyhWPdNCd4vP1LyBVbKuaZJgqXeEi6Xb4%3D'

        # space - testing
        # url = 'https://chat.googleapis.com/v1/spaces/AAAAJlaLdfc/messages?key=AIzaSyDdI0hCZtE6vySjMm-WEfRq3CPzqKqqsHI&token=icsth9LJGIi9jQPrp5UCdAqw2pByc12XVqv_ySGL69k%3D'

        message = f'[{report["report_name"]}]'
        if not status:
            message += ' Auto switched to datamart.'
        else:
            message += ' Auto switched to non-datamart.'

        message += f' Latest Data is : {latest_data}'

        bot_message = {'text' : message}
        message_headers = {'Content-Type': 'application/json; charset=UTF-8'}
        http_obj = Http()
        
        response_1 = http_obj.request(
            uri=url,
            method='POST',
            headers=message_headers,
            body=dumps(bot_message),
        )
                
        response_2 = http_obj.request(
            uri=url_2,
            method='POST',
            headers=message_headers,
            body=dumps(bot_message),
        )
