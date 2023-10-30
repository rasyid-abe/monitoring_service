from django.utils import timezone
from datetime import timedelta
from django.shortcuts import redirect
from django.db.models import Q
from django.views.generic import View
from django.http import JsonResponse
from apps.home.Models.apps import \
    Alert, \
    AlertDetail, \
    AlertHistory, \
    SettingMapping

class AlertApis(View):

    @classmethod
    def get_alert_list(cls):
        
        alert_list = Alert.objects \
            .order_by('alert_name') \
            .values('id', 'alert_name',
                'status', 'updated_at')

        for item in alert_list:
            item['latest_error'] = cls.get_latest_error(item['id'])

        configuration_list = cls.get_configurations()

        return alert_list, configuration_list
    
    @classmethod
    def get_latest_error(cls, id):
        
        try:
            latest_error = AlertHistory.objects \
                .filter(id_alert_detail__id_alert_id=id) \
                .values('created_at') \
                .last()['created_at']
        
        except:
            return '-'
        
        return latest_error
    
    @classmethod
    def get_configurations(cls):
        settings = SettingMapping.objects \
            .filter(
                Q(setting_name__icontains='etl_data_threshold') |
                Q(setting_name__icontains='etl_execution_threshold')
            ) \
            .order_by('id')
        return settings

    @classmethod
    def get(cls, request):
        """
        get detail and error alert || update status 
        """
        
        purpouse = request.GET['purpouse']
        id = request.GET['id']

        result = []

        if purpouse == 'etl':
            result = cls.get_alert_detail_list(id)
        elif purpouse == 'history':
            result = cls.get_alert_history(id)
        elif purpouse == 'update-alert':
            try:
                status = request.GET['status']
                cls.update_alert_status(id, status)
                return JsonResponse({'status' : 200, 'message' : 'Update Status Successful'})
            except:
                return JsonResponse({'status' : 500, 'message' : 'Internal Error'})
        elif purpouse == 'update-alert-detail':
            try:
                status = request.GET['status']
                cls.update_alert_detail_status(id, status)
                return JsonResponse({'status' : 200, 'message' : 'Update Status Successful'})
            except:
                return JsonResponse({'status' : 500, 'message' : 'Internal Error'})
        elif purpouse == 'update-alert-detail-detail':
            try:
                detail = request.GET['detail']
                cls.update_alert_detail_detail(id, detail)
                return JsonResponse({'status' : 200, 'message' : 'Update Detail Successful'})
            except:
                return JsonResponse({'status' : 500, 'message' : 'Internal Error'})

        alert_name = Alert.objects.filter(id=id).values('alert_name')[0]['alert_name']

        return JsonResponse({
            'status' : 200,
            'data': 
                {
                    'alert_name' : alert_name,
                    'alert_detail' : list(result)
                }
        })
    
    @classmethod
    def post(cls, request):
        
        threshold = request.POST['threshold']
        id = request.POST['id']

        setting = SettingMapping.objects \
            .get(id=id)
        
        setting.value = {"threshold_in_minute": int(threshold)}
        setting.save()

        return redirect('alert.html')

    @classmethod
    def get_alert_detail_list(cls, id):

        result = AlertDetail.objects \
            .filter(id_alert_id=id) \
            .values('id', 'alert_detail_name', 'status', 'created_at',
            'updated_at', 'detail') \
            .order_by('alert_detail_name')

        return result
    
    @classmethod
    def get_alert_history(cls, id):

        result = AlertHistory.objects \
            .filter(id_alert_detail__id_alert_id=id) \
            .values('id_alert_detail__alert_detail_name', 'type', 'message', 'created_at') \
            .order_by('-created_at', 'id_alert_detail__alert_detail_name')

        return result
    
    @classmethod
    def update_alert_status(cls, id, status):

        alert = Alert.objects.get(id=id)
        alert.status = status
        alert.updated_at = (timezone.localtime() + timedelta(hours=7)).replace(tzinfo=None)
        alert.save()
    
    @classmethod
    def update_alert_detail_status(cls, id, status):

        alert_detail = AlertDetail.objects.get(id=id)
        alert_detail.status = status
        alert_detail.updated_at = timezone.localtime()
        alert_detail.save()

    @classmethod
    def update_alert_detail_detail(cls, id, detail):

        if '0' in detail:
            detail = {"type":0}
        else:
            detail = {"type":1}

        alert_detail = AlertDetail.objects.get(id=id)
        alert_detail.detail = detail
        alert_detail.updated_at = timezone.localtime()
        alert_detail.save()
