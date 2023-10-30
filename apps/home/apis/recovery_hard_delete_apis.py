from datetime import datetime
from django.views.generic import View
from django.http import JsonResponse
from apps.home.Models.apps import *
from apps.home.Models.airflow import *
from apps.home.Models.etl_history import *
from apps.home.Models.recovery_history import *
from django.db.models import Q, Count, Sum
from django.db import transaction
import json
from datetime import timedelta

class RecoveryHardDeleteApis(View):


    @classmethod
    def get_recovery_histories(cls):
        # get recovery history
        histories = RecoveryHistoryHardDelete.objects \
            .using('datamart_postgres') \
            .exclude(id = 1) \
            .order_by('-id') \
            .values()[:100]

        max_deleted_at = histories.values_list('actdate', flat=True)
        max_deleted_at = max(max_deleted_at)

        total_covered = RecoveryHistoryHardDelete.objects \
            .using('datamart_postgres') \
            .count()

        # get unrecovered data
        unrecovered = TransactionsHistory.objects \
            .using('datamart_postgres') \
            .filter(createdate_datalake__gt = max_deleted_at) \
            .order_by('-createdate_datalake') \
            .values()
        
        for item in unrecovered:
            item['transaction_tgl'] += timedelta(hours=7)
            item['createdate_datalake'] += timedelta(hours=7)

        for item in histories:
            succeed, failed = cls.get_detail_count(item['params'])
            item['actdate'] += timedelta(hours=7)
            item['succeed'] = succeed
            item['failed'] = failed
            
        return histories, unrecovered, total_covered

    @classmethod
    def get_detail_count(cls, params):
        succeed = 0
        failed = 0

        for _, value in params.items():
            
            if not 'status' in value:
                failed += 1
                continue

            if value['status'] != 'success':
                failed += 1
                continue

            succeed += 1

        return succeed, failed

