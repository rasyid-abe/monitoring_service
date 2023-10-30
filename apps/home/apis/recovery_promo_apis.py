from datetime import datetime
from django.views.generic import View
from django.http import JsonResponse
from apps.home.Models.apps import *
from apps.home.Models.airflow import *
from apps.home.Models.etl_history import *
from apps.home.Models.recovery_history import *
from django.db.models import F, Sum
from django.db import transaction
import json
from datetime import timedelta

class RecoveryPromoApis(View):


    @classmethod
    def get_recovery_histories(cls):
        # get recovery history
        histories = RecoveryHistoryPromo.objects \
            .using('datamart_postgres') \
            .order_by('-id') \
            .values()[:100]

        recovery_counts = cls.get_detail_count()
            
        return histories, recovery_counts

    @classmethod
    def get_detail_count(cls):
        # Melakukan penghitungan untuk is_recovered_product
        recovered_product_count = RecoveryHistoryPromo.objects \
            .using('datamart_postgres') \
            .filter(is_recovered_product=True) \
            .count()

        # Melakukan penghitungan untuk is_recovered_promo
        recovered_promo_count = RecoveryHistoryPromo.objects \
            .using('datamart_postgres') \
            .filter(is_recovered_promo=True) \
            .count()

        # Melakukan penghitungan untuk is_recovered_compliment
        recovered_compliment_count = RecoveryHistoryPromo.objects \
            .using('datamart_postgres') \
            .filter(is_recovered_compliment=True) \
            .count()
        
        total_count = RecoveryHistoryPromo.objects \
            .using('datamart_postgres') \
            .count()
        
        recovery_counts = \
        {
            'product_count': recovered_product_count,
            'promo_count': recovered_promo_count,
            'compliment_count': recovered_compliment_count,
            'total_count' : total_count
        }

        return recovery_counts
