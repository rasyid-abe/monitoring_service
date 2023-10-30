from datetime import timedelta
from django.apps import apps
from django.views.generic import View
from django.http import JsonResponse
from django.utils import timezone
from apps.home.Models.etl_history import *
from apps.home.Models.klopos import *
from core.settings import \
    COCKPIT_ENDPOINT, \
    COCKPIT_USERNAME, \
    COCKPIT_PASSWORD
import json
import requests

class EtlStatusAPis(View):

    @classmethod
    def get_report_list(cls):
        
        report_list = DashboardReportStatus.objects \
            .using('datamart_postgres') \
            .order_by('report_name') \
            .values()
        
        cms_ids = [item['id_m_cms_menu'] for item in report_list]
        cms_data = cls.get_report_status(cms_ids)

        # get execution history
        all_models = apps.get_models()
        history_map = {}
        for item in all_models:
            if 'raw' in item._meta.db_table:
                history_map[item._meta.db_table] = item.__name__

        for item in report_list:

            # get latest ETL data
            item['ts_end'] = '?'

            try:
                item['ts_end'] = cls.get_latest_data(history_map[item['history_table_name']])
            except:
                pass

            # get report status (using datamart or not)
            item['status'] = '?'

            try:
                if cms_data[item['id_m_cms_menu']] == item['datamart_url']:
                    item['status'] = 'Datamart'
                
                elif cms_data[item['id_m_cms_menu']] == item['non_datamart_url']:
                    item['status'] = 'Non-Datamart'
            except:
                pass

        return report_list

    @classmethod
    def get_latest_data(cls, model):

        model = apps.get_model('home', model)        
        latest_data = model.objects \
            .using('datamart_postgres') \
            .order_by('ts_end') \
            .last()
        
        return latest_data.ts_end + timedelta(hours=7)

    @classmethod
    def get_report_status(cls, cms_ids):
        
        data = MCMSMenuRetina.objects \
            .using('klopos') \
            .filter(id_m_cms_menu__in = cms_ids) \
            .values('id_m_cms_menu', 'm_cms_menu_url')
        
        data_dict = {}
        for item in data:
            data_dict[item['id_m_cms_menu']] = item['m_cms_menu_url']
                
        return data_dict
    
    @classmethod
    def get(cls, request):

        purpose = request.GET.get('purpose')
        id = request.GET.get('id')
        status = request.GET.get('status')

        if 'is_automate' in purpose:
            try:
                cls.change_auto_switch_status(id, status)
            
                return JsonResponse({
                    'status' : 200,
                    'message': 'Update State Successful'
                })
            except:
                return JsonResponse({
                    'status' : 500,
                    'message': 'Update State Failed'
                })
        
        if 'datamart' in purpose:
            try:
                status, msg = cls.switch_datamart(id, status)
                return JsonResponse({
                    'status' : status,
                    'message': msg
                })
            except:
                return JsonResponse({
                    'status' : 500,
                    'message': 'Update Failed'
                })
            
    @classmethod
    def change_auto_switch_status(cls, id, status):

        report_map = DashboardReportStatus.objects \
            .using('datamart_postgres') \
            .get(id=id)
        
        report_map.updated_at = timezone.localtime()
        report_map.is_automate = status
        report_map.save()
    
    @classmethod
    def switch_datamart(cls, id_m_cms_menu, status):
        
        token = cls.get_cockpit_token()
        menu = cls.get_cockpit_menu(token, id_m_cms_menu)

        table_map = DashboardReportStatus.objects \
            .using('datamart_postgres') \
            .get(id_m_cms_menu=id_m_cms_menu)
        
        if status == 'True':
            menu['content'] = table_map.datamart_url
        elif status == 'False':
            menu['content'] = table_map.non_datamart_url
        
        # standarize payload
        menu['seq'] = menu['urutan']
        menu['is_android_transactional'] = int(menu['is_android_transactional'])
        menu['is_menu_mobile'] = bool(int(menu['is_android_transactional']))
        menu['is_display'] = bool(int(menu['menu_is_display']))
        menu['method'] = json.dumps(menu['method'], separators=(',', ':'))  

        url = COCKPIT_ENDPOINT + 'api_santan/0_0_1/menu_internal/menu_cms_retina'
        head = \
        {
            'Token': token,
            'Content-Type': 'application/json'
        }

        result = requests.put(url, headers=head, data=json.dumps(menu))

        return result.status_code, result.json()['msg']
    
    @classmethod
    def get_cockpit_menu(cls, token, id_m_cms_menu):

        url = COCKPIT_ENDPOINT + 'api_santan/0_0_1/menu_internal/menu_cms_retina'
        head = \
        {
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Accept': '*/*',
            'Token': token
        }

        menus = requests.get(url, headers=head).json()['data']
        result = None

        id_m_cms_menu = str(id_m_cms_menu)
        for menu in menus:
            if menu['id'] == id_m_cms_menu:
                result = menu
                break

        return result

    @classmethod
    def get_cockpit_token(cls):

        url = COCKPIT_ENDPOINT + 'api_santan/0_0_1/internal/login'
        head = \
        {
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Accept': '*/*',
        }
        body = \
        {
            'email' : COCKPIT_USERNAME,
            'password' : COCKPIT_PASSWORD
        }

        token = requests.post(url, headers=head, data=body).json()

        return token['token']