import asyncio
from django.urls import path, re_path
from apps.home import views
from apps.home.apis.alert_apis import AlertApis
from apps.home.apis.airflow_apis import AirflowApis
from apps.home.apis.dashboard_apis import DashboardApis
from apps.home.apis.cdc_apis import CdcApis
from apps.home.apis.nifi_apis import NifiApis
from apps.home.apis.etl_apis import EtlAPis
from apps.home.apis.etl_status_apis import EtlStatusAPis
from apps.home.apis.validity_and_recovery_apis import ValidityAndRecoveryApis
from apps.home.apis.etl_caller_apis import ETLCallerApis
from apps.home.scheduler import start_jobs
from apps.home.jobs import etl_caller

urlpatterns = [

    # The home page
    path('', views.index, name='home'),

    # Apis
    path('apis/alert', AlertApis.as_view(), 
        name='apis-alert'),

    path('apis/airflow/taks', AirflowApis.as_view(), 
        name='apis-airflow-tasks'),

    path('apis/nifi/processors', NifiApis.as_view(), 
        name='apis-nifi-processor'),
    
    path('apis/etl/histories', EtlAPis.as_view(), 
        name='apis-etl-histories'),
    
    path('apis/etl-status', EtlStatusAPis.as_view(), 
        name='apis-etl-status'),
    
    path('apis/dashboard', DashboardApis.as_view(), 
        name='apis-dashboard'),
    
    path('apis/validity-and-recovery', ValidityAndRecoveryApis.as_view(), 
        name='apis-validity-and-recovery'),

    path('apis/cdc', CdcApis.as_view(), 
        name='apis-cdc'),

    path('apis/cdc/restart', CdcApis.restart,
        name='apis-cdc-restart'),
    
    path('apis/etl-caller', ETLCallerApis.as_view(),
        name='apis-etl-caller'),

    # Matches any html file
    re_path('^(?!.*\bapis\b).*$', views.pages, name='pages'),
]

etl_caller.reset_state()
start_jobs()