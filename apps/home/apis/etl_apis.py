from datetime import timedelta
from django.db.models import Sum
from django.views.generic import View
from django.http import JsonResponse
from django.utils import timezone
from apps.home.Models.apps import *
from apps.home.Models.airflow import *
from apps.home.Models.etl_history import *
from apps.home.Models.recovery_history import *
import json

class EtlAPis(View):

    objects = \
    {
        'Akunting' : RawDatamartAccountingHistory,
        'Akunting V2' : RawDatamartAkuntingV2History,
        'Akunting - Jurnal' : RawDatamartJournalHistory,
        'Akunting - Hutang' : RawDatamartJurnalHutangHistory,
        'Akunting - Piutang' : RawDatamartJurnalPiutangHistory,
        'Batch & Serial Number' : RawDatamartBatchSerialNumberHistory,
        'Busiest Item Time' : RawDatamartBusiestItemTimeHistory,
        'Busiest Selling Time' : RawDatamartBusiestSellingTimeHistory,
        'BI - Submission Wallet' : RawDatamartSubmissionWalletHistory,
        'BI - Merchant Outlet' : RawDatamartMerchantOutletHistory,
        'BI - Transaction Payment' : RawDatamartTransactionPaymentHistory,
        'BI - Transaction Type' : RawDatamartTransactionTypeHistory,
        'BI - Transaction Wallet Dynamic' :RawDatamartTrasactionWalletDynamicHistory,
        'Cashier' : RawDatamartCashierHistory,
        'Compliment' : RawDatamartComplimentHistory,
        'Daily Report' : RawDatamartDailyReportHistory,
        'Dashboard' : RawDatamartSalesDashboardHistory,
        'Extras (Addon & Addon Detail V2)' : RawDatamartSubextrasHistory,
        'Merchant Transaction' : RawDatamartMerchantTransactionHistory,
        'Outlet Sales V2' : RawDatamartOutletSalesHistory,
        'Order Type' : RawDatamartOrderTypeHistory,
        'Payment Type' : RawDatamartPaymentTypeHistory,
        'Product V2 (kolom refund)' : RawDatamartProductSalesRefundHistory,
        'Promo' : RawDatamartPromoHistory,
        'Submission Ecommerce Grabfood' : RawDatamartSubmissionEcommerceGrabfoodHistory,
        'Support Trx' : RawDatamartSupportTrxHistory,
        'Utilization' : RawDatamartUtilizationHistory
    }

    @classmethod
    def get_elt_histories(cls):

        datamart_postgres = {}
        for key, object in cls.objects.items():
            try:
                data = object.objects.using('datamart_postgres').last()
                data.actdate += timedelta(hours=7)
                data.ts_end += timedelta(hours=7)
                if 'dag_id' in data.params:
                    data.type = 'Airflow'
                else:
                    data.type = 'Spark'

                datamart_postgres[key] = data
            except:
                pass

        return datamart_postgres

    @classmethod
    def get(cls, request):
        # get etl_histories (100 rows data)

        database = request.GET['database']
        purpose = request.GET.get('purpose')
        data = []

        if not purpose:
            etl_type = request.GET['type']
            try:
                data = cls.objects[etl_type].objects.using(database).order_by('-id').values()[:100]

                if database == 'datamart_postgres':
                    for item in data:
                        item['actdate'] += timedelta(hours=7)
                        item['ts_end'] += timedelta(hours=7)
                        item['ts_current'] += timedelta(hours=7)
                        item['time_process'] = '{:>12,.2f}'.format(item['time_process'] / 60000)
                        item['num_row'] = f'{int(item["num_row"]):,}'

                data = list(data)

            except:
                pass
        else:
                data = cls.get_etl_performance()
                data = list(data)

        return JsonResponse({
                'status' : 200,
                'data': data
            })

    @classmethod
    def get_etl_performance(cls):

        current_time = (timezone.localtime()).timestamp()
        datamart_postgres = {}
        estimation_time = 0
        for key, object in cls.objects.items():
            try:
                data = object.objects.using('datamart_postgres') \
                    .order_by('-id') \
                    .values('num_row', 'time_process', 'params', 'ts_end').all()[:50]

                datamart_postgres[key] = list(data)
            except:
                pass

        for key, item in datamart_postgres.items():
            try:
                performance = round(sum([x['num_row'] for x in item]) / \
                    (sum([x['time_process'] for x in item]) / 60000), 0)
                performance = f'{int(performance):,}'
            except:
                performance = 0

            try:
                execution_time = []
                for i in item:
                    sequence = int(json.loads(i['params'] \
                        .replace('sequence','') \
                        .replace('min','') \
                        .replace('hourlyupdate', '60') \
                        .replace('dailyupdate', '1440') \
                        )['fn'])

                    execution_time.append(i['time_process'] / 60000 / sequence)

                execution_time = round(sum(execution_time) / len(execution_time), 4)

                if execution_time > 1:
                    estimation_time = '∞'
                else:
                    latest_data = (item[0]['ts_end']).timestamp()
                    minus_data = (current_time - latest_data) / 60
                    estimation_time = round(((minus_data / ( 1 / execution_time)) * 2) / 60, 4)
            except:
                execution_time = '-'
                estimation_time = '-'

            datamart_postgres[key] = \
            {
                'performance' : performance,
                'execution_time' : execution_time,
                'estimation_time' : estimation_time,
                'estimation_time_day' : estimation_time,
            }

            if(estimation_time not in ['-', '∞']):
                datamart_postgres[key]['estimation_time_day'] = int(float(estimation_time) / 24)

        return datamart_postgres.items()
