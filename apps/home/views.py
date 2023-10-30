# -*- encoding: utf-8 -*-
from datetime import timedelta
from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.utils import timezone
from django.urls import reverse
from apps.home.apis.airflow_apis import AirflowApis
from apps.home.apis.alert_apis import AlertApis
from apps.home.apis.etl_apis import EtlAPis
from apps.home.apis.etl_status_apis import EtlStatusAPis
from apps.home.apis.nifi_apis import NifiApis
from apps.home.apis.cdc_apis import CdcApis
from apps.home.apis.validity_and_recovery_apis import ValidityAndRecoveryApis
from apps.home.apis.recovery_apis import RecoveryApis
from apps.home.apis.recovery_hard_delete_apis import RecoveryHardDeleteApis
from apps.home.apis.recovery_promo_apis import RecoveryPromoApis
from apps.home.apis.etl_caller_apis import ETLCallerApis
from core.settings import VALIDITY_ENDPOINT


@login_required(login_url="/login/")
def index(request):

    context = \
    {
        'segment': 'index'
    }

    html_template = loader.get_template('home/index.html')
    return HttpResponse(html_template.render(context, request))


@login_required(login_url="/login/")
def pages(request):
    context = {}
    try:
        load_template = request.path.split('/')[-1]

        if load_template == 'admin':
            return HttpResponseRedirect(reverse('admin:index'))
        context['segment'] = load_template

        if load_template == 'airflow.html':
            identity, dag_list, general_error, failed_task = AirflowApis.get_airflow_status()
            context = \
            {
                'segment': 'airflow',
                'identity' : identity,
                'dag_list': dag_list,
                'general_error' : general_error,
                'failed_task' : failed_task,
                'dag_list_length': len(dag_list)
            }
        
        if load_template == 'alert.html':
            alert_list, configuration_list = AlertApis.get_alert_list()
            context = \
            {
                'segment': 'alert',
                'alert_list' : alert_list,
                'configuration_list' : configuration_list
            }

        if load_template == 'etl.html':
            etl_data_postgres = EtlAPis.get_elt_histories()
            configurations = AlertApis.get_configurations()
        
            context = \
            {
                'segment': 'etl_data_movement',
                'etl_data_postgres': etl_data_postgres,
                'configurations': configurations,
                'etl_threshold': (timezone.localtime() - timedelta(minutes=configurations[1].value['threshold_in_minute'])).replace(tzinfo=None),
                'data_threshold': (timezone.localtime() - timedelta(minutes=configurations[0].value['threshold_in_minute'])).replace(tzinfo=None)
            }
        
        if load_template == 'etl_status.html':
            report_list = EtlStatusAPis.get_report_list()
        
            context = \
            {
                'segment': 'etl_data_status',
                'report_list': report_list,
                'data_threshold': (timezone.localtime() - timedelta(days=1)).replace(tzinfo=None)
            }

        if load_template == 'nifi.html':
            endpoint, identity, process_list = NifiApis.get_nifi_status()
            context = \
            {
                'segment' : 'scheduler_nifi',
                'identity' : identity,
                'endpoint' : endpoint,
                'process_list': process_list,
                'process_list_length': len(process_list),
            }
        
        if load_template == 'cdc-status.html':
            identity, connector_list = CdcApis.get_cdc_status()
            context = \
            {
                'segment': 'cdc-status',
                'identity' : identity,
                'connectors' : connector_list,
                'connectors_length': len(connector_list),
            }

        if load_template == 'cdc-data.html':
            dispute_table_count, cdc_list = CdcApis.get_cdc_data()
            context = \
            {
                'segment': 'cdc-data',
                'cdc_list' : cdc_list,
                'validity_endpoint' : VALIDITY_ENDPOINT + '/validity/cdc',
                'dispute_table_count' : dispute_table_count
            }

        if load_template == 'recovery.html':
            recovery_urls = RecoveryApis.get_recovery_url()
            context = \
            {
                'segment': 'execute_recovery',
                'recovery_urls' : recovery_urls,
            }

        if load_template == 'validity_and_recovery.html':
            validity_list, recovery_list, waiting, recovered, schedulers = ValidityAndRecoveryApis.get_histories()
            context = \
            {
                'segment': 'validity_and_recovery',
                'validity_list' : validity_list,
                'recovery_list' : recovery_list,
                'waiting' : waiting,
                'recovered' : recovered,
                'schedulers' : schedulers
            }
        
        if load_template == 'recovery_hard_delete.html':
            histories, unrecovered, total_covered = RecoveryHardDeleteApis.get_recovery_histories()
            context = \
            {
                'segment': 'recovery_hard_delete',
                'histories' : histories,
                'recovered' : total_covered,
                'unrecovered' : unrecovered,
                'unrecovered_length' : len(unrecovered)
            }

        if load_template == 'recovery_promo.html':
            histories, recovery_counts = RecoveryPromoApis.get_recovery_histories()
            context = \
            {
                'segment': 'recovery_promo',
                'histories' : histories,
                'recovery_counts' : recovery_counts
            }

        if load_template == 'etl_caller.html':
            etl_list, active_etl, innactive_etl = ETLCallerApis.get_elt_list()
            context = \
            {
                'segment': 'scheduler_etl_caller',
                'active_etl': active_etl,
                'innactive_etl': innactive_etl,
                'etl_list' : etl_list
            }
        
        html_template = loader.get_template('home/' + load_template)
        return HttpResponse(html_template.render(context, request))

    except template.TemplateDoesNotExist:

        html_template = loader.get_template('defaults/page-404.html')
        return HttpResponse(html_template.render(context, request))

    except:
        html_template = loader.get_template('defaults/page-500.html')
        return HttpResponse(html_template.render(context, request))
