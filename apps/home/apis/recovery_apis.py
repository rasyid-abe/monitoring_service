import requests
from datetime import timedelta

from apps.home.Models.apps import *
from apps.home.Models.airflow import *
from apps.home.Models.etl_history import *
from apps.home.Models.recovery_history import *
from django.http import JsonResponse, HttpResponseRedirect
from core.settings import KAFKA_ENDPOINT
from django.views.generic import View

class RecoveryApis(View):

    @classmethod
    def get_recovery_url(cls):

        recovery_urls = RecoveryMapping.objects.order_by('etl_name').all()

        return recovery_urls
    