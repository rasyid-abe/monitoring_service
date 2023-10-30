from datetime import timedelta
from django.shortcuts import redirect
from django.views.generic import View
from django.http import JsonResponse
from django.utils import timezone
from apps.home.Models.etl_history import ETLList
import json

class ETLCallerApis(View):

    @classmethod
    def get_elt_list(cls):
        
        active_etl = 0
        innactive_etl = 0
        etl_list = ETLList.objects.using('datamart_postgres') \
            .order_by('etl_name') \
            .all()

        for etl in etl_list:
            if etl.is_active:
                active_etl += 1
            else:
                innactive_etl += 1

        return etl_list, active_etl, innactive_etl

    @classmethod
    def get(cls, request):
        purpose = request.GET.get('purpose')
        id = request.GET.get('id')

        # change is_active
        if 'is_active' in purpose:
            try:
                status = request.GET.get('status')
                cls.update_is_active(id, status)
                return JsonResponse({'status' : 200, 'message' : 'Update Status Successful'})
            except:
                return JsonResponse({'status' : 500, 'message' : 'Internal Error'})
    
    @classmethod
    def post(cls, request):

        etl_name = request.POST.get('etl_name')
        endpoint = request.POST.get('endpoint')
        id = request.POST.get('id')
        
        # new data
        if not id:
            cls.create_new_etl(etl_name, endpoint)
        else:
            # update data
            cls.update_endpoint(id, etl_name, endpoint)

        return redirect('etl_caller.html')


    @classmethod
    def update_endpoint(cls, id, etl_name, new_endpoint):
        etl_record = ETLList.objects.using('datamart_postgres').get(id=id)
        etl_record.etl_name = etl_name
        etl_record.endpoint = new_endpoint
        etl_record.updated_at = (timezone.localtime() + timedelta(hours=7)).replace(tzinfo=None)
        etl_record.save()

    @classmethod
    def update_is_active(cls, id, status):
        etl_record = ETLList.objects.using('datamart_postgres').get(id=id)
        etl_record.is_active = status
        etl_record.updated_at = (timezone.localtime() + timedelta(hours=7)).replace(tzinfo=None)
        etl_record.save()

    @classmethod
    def create_new_etl(cls, etl_name, endpoint):
        etl_record = ETLList(etl_name=etl_name, endpoint=endpoint, is_active=False, is_running=False)
        etl_record.save(using='datamart_postgres')
