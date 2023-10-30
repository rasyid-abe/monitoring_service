from datetime import datetime
from django.views.generic import View
from django.http import JsonResponse
from apps.home.Models.apps import *
from apps.home.Models.airflow import *
from apps.home.Models.etl_history import *
from apps.home.Models.recovery_history import *
from django.db.models import Q, Count, Sum
from django.db import transaction

from apps.home.apis.nifi_apis import NifiApis

class ValidityAndRecoveryApis(View):

    @classmethod
    def get_histories(cls):

        validities = cls.get_validity_histories() 
        recoveries = cls.get_recovery_histories()
        schedulers = cls.get_schedulers()
        waiting = 0
        recovered = 0

        for recovery_name, recovery_value in recoveries.items():
            recovered += recovery_value['is_recovered']
            for validity_name, validity_value in validities.items():
                if recovery_name == validity_name:
                    waiting += validity_value['is_waiting']
                    recovery_value['recovering'] = validity_value['is_waiting']
                    break

        return validities, recoveries, waiting, recovered, schedulers

    @classmethod
    def get_schedulers(cls):

        data = ValidityAndRecoveryScheduler.objects \
            .order_by('start_at', 'end_at', 'etl_name', 'recovery_name') \
            .all()

        return data
    
    @classmethod
    def get_recovery_histories(cls):
        
        result = {}
        objects = \
        {
            'Accounting' : RecoveryHistoryDatamartAkunting,
            'Busiest Selling Time' : RecoveryHistoryDatamartBusiestSellingTime,
            'Product' : RecoveryHistoryDatamartProduk,
            'Sub Variant' : RecoveryHistoryDatamartSubVarian,
            'Variant' : RecoveryHistoryDatamartVarian
        }

        for key, object in objects.items():
            try:
                data = object.objects.using('datamart_postgres').last()
                status = object.objects.using('datamart_postgres').count()
                data = \
                {
                    'act_date' : data.act_date,
                    'is_recovered' : status,
                    'recovering' : 0
                }
                result[key] = data
            except:
                pass
        
        return result
    
    @classmethod
    def get_validity_histories(cls):
        
        result = {}
        objects = \
        {
            'Accounting' : ValidityHistoryAkunting,
            'Busiest Selling Time' : ValidityHistoryBusiestSellingTime,
            'Product' : ValidityHistoryProduk,
            'Sub Variant' : ValidityHistorySubVarian,
            'Variant' : ValidityHistoryVarian,
            'Busiest Time' : ValidityHistoryWaktuTeramai
        }

        for key, object in objects.items():
            try:
                data = object.objects.using('datamart_postgres').last()
                is_waiting_count = object.objects.using('datamart_postgres') \
                        .filter(is_recovery = 0) \
                        .count()
                data = \
                {
                    'ts_current' : data.ts_current,
                    'actdate' : data.actdate,
                    'is_waiting' : is_waiting_count
                }
                result[key] = data
            except:
                pass

        return result

    
    @classmethod
    def get(cls, request):
        data_type = request.GET.get('data_type')
        type = request.GET.get('type')
        start_time = request.GET.get('start_time')
        end_time = request.GET.get('end_time')
        data = []

        if data_type == 'Recovery':
            objects = \
            {
                'Accounting' : RecoveryHistoryDatamartAkunting,
                'Busiest Selling Time' : RecoveryHistoryDatamartBusiestSellingTime,
                'Product' : RecoveryHistoryDatamartProduk,
                'Sub Variant' : RecoveryHistoryDatamartSubVarian,
                'Variant' : RecoveryHistoryDatamartVarian
            }

            data = objects[type].objects.using('datamart_postgres') \
                    .filter(Q(act_date__lte=end_time) & Q(act_date__gte=start_time)) \
                    .values('id_user', 'id_cabang') \
                    .annotate(total=Count('id'), rows=Sum('num_row')) \
                    .order_by('id_user', 'id_cabang',)

        if data_type == 'Validity':
            objects = \
            {
                'Accounting' : ValidityHistoryAkunting,
                'Busiest Selling Time' : ValidityHistoryBusiestSellingTime,
                'Product' : ValidityHistoryProduk,
                'Sub Variant' : ValidityHistorySubVarian,
                'Variant' : ValidityHistoryVarian,
                'Busiest Time' : ValidityHistoryWaktuTeramai
            }

            data = objects[type].objects.using('datamart_postgres') \
                    .filter(Q(actdate__lte=end_time) & Q(actdate__gte=start_time)) \
                    .values('id_user', 'id_cabang', 'is_recovery') \
                    .annotate(total=Count('id')) \
                    .order_by('id_user', 'id_cabang', 'is_recovery')
            
        if data_type == 'Nifi_Group':
            _, _, data = NifiApis.get_nifi_status()

            recovery = [] 
            etl = []
            for item in [x['name'] for x in data]:
                if 'recovery' in item.lower():
                    recovery.append(item)
                else:
                    etl.append(item)
            
            data = {'recovery' : recovery, 'etl' : etl}

        return JsonResponse({
                'status' : 200,
                'data': data
            })

    @classmethod
    @transaction.atomic
    def post(cls, request):
        try:
            ValidityAndRecoveryScheduler.objects.all().delete()
            index = 1
            for _, values in request.POST.lists():
                cron_state = 0

                if 'no' in values[4].lower():
                    cron_state = -1 
                
                object = ValidityAndRecoveryScheduler(
                    id=index,
                    etl_name = values[0],
                    recovery_name = values[1],
                    start_at = values[2],
                    end_at = values[3],
                    cron_state = cron_state,
                    created_at = datetime.now()
                )
                object.save()
                index += 1
            
            return JsonResponse({
                'status' : 200,
                'message': 'Schedulers has been successfully saved to the database'
            })            
        except:
            return JsonResponse({
                'status' : 400,
                'message': 'Error'
            })