from django.db import models

class DatamartHistory(models.Model):
    actdate = models.DateTimeField()
    ts_current = models.DateTimeField()
    ts_end = models.DateTimeField()
    num_row = models.IntegerField()
    time_process = models.FloatField()
    params = models.TextField()

    class Meta:
        abstract = True

class RawDatamartAccountingHistory(DatamartHistory):
    class Meta:
        managed = False
        db_table = 'raw_datamart_accounting_history'

class RawDatamartBusiestItemTimeHistory(DatamartHistory):
    class Meta:
        managed = False
        db_table = 'raw_datamart_busiest_item_time_history'

class RawDatamartBusiestSellingTimeHistory(DatamartHistory):
    class Meta:
        managed = False
        db_table = 'raw_datamart_busiest_selling_time_history'

class RawDatamartCashierHistory(DatamartHistory):
    class Meta:
        managed = False
        db_table = 'raw_datamart_cashier_history'

class RawDatamartComplimentHistory(DatamartHistory):
    class Meta:
        managed = False
        db_table = 'raw_datamart_compliment_history'

class RawDatamartMerchantOutletHistory(DatamartHistory):
    class Meta:
        managed = False
        db_table = 'raw_datamart_merchant_outlet_history'

class RawDatamartPromoHistory(DatamartHistory):
    class Meta:
        managed = False
        db_table = 'raw_datamart_promo_history'

class RawDatamartSubmissionEcommerceGrabfoodHistory(DatamartHistory):
    class Meta:
        managed = False
        db_table = 'raw_datamart_submission_ecommerce_grabfood_history'

class RawDatamartSubmissionWalletHistory(DatamartHistory):
    class Meta:
        managed = False
        db_table = 'raw_datamart_submission_wallet_history'

class RawDatamartSupportTrxHistory(DatamartHistory):
    class Meta:
        managed = False
        db_table = 'raw_datamart_support_trx_history'

class RawDatamartTransactionHistory(DatamartHistory):
    class Meta:
        managed = False
        db_table = 'raw_datamart_transaction_history'

class RawDatamartTransactionPaymentHistory(DatamartHistory):
    class Meta:
        managed = False
        db_table = 'raw_transaction_type_payment_history'

class RawDatamartTransactionTypeHistory(DatamartHistory):
    class Meta:
        managed = False
        db_table = 'raw_transaction_type_payment_history'

class RawDatamartTrasactionWalletDynamicHistory(DatamartHistory):
    class Meta:
        managed = False
        db_table = 'raw_datamart_transaction_wallet_dynamic_history'

class RawDatamartProductSalesRefundHistory(DatamartHistory):
    class Meta:
        managed = False
        db_table = 'raw_datamart_product_sales_refund_history'

class RawDatamartOutletSalesHistory(DatamartHistory):
    class Meta:
        managed = False
        db_table = 'raw_datamart_outlet_sales_history'

class RawDatamartJournalHistory(DatamartHistory):
    class Meta:
        managed = False
        db_table = 'raw_datamart_journal_history'

class RawDatamartSubextrasHistory(DatamartHistory):
    class Meta:
        managed = False
        db_table = 'raw_datamart_subextra_history'

class RawDatamartOrderTypeHistory(DatamartHistory):
    class Meta:
        managed = False
        db_table = 'raw_datamart_order_type_history'

class RawDatamartUtilizationHistory(DatamartHistory):
    class Meta:
        managed = False
        db_table = 'raw_datamart_utilization_history'

class RawDatamartBatchSerialNumberHistory(DatamartHistory):
    class Meta:
        managed = False
        db_table = 'raw_datamart_batchserial_number_history'

class RawDatamartSalesDashboardHistory(DatamartHistory):
    class Meta:
        managed = False
        db_table = 'raw_datamart_sales_dashboard_history'

class RawDatamartDailyReportHistory(DatamartHistory):
    class Meta:
        managed = False
        db_table = 'raw_datamart_daily_report_history'

class RawDatamartJurnalHutangHistory(DatamartHistory):
    class Meta:
        managed = False
        db_table = 'raw_datamart_jurnal_hutang_history'

class RawDatamartJurnalPiutangHistory(DatamartHistory):
    class Meta:
        managed = False
        db_table = 'raw_datamart_jurnal_piutang_history'

class RawDatamartAkuntingRecoveryHistory(DatamartHistory): # Obsolete / tidak dipakai
    class Meta:
        managed = False
        db_table = 'raw_datamart_live_recovery_accounting_history'

class RawDatamartAkuntingV2History(DatamartHistory):
    class Meta:
        managed = False
        db_table = 'raw_datamart_jurnal_history_v2'

class RawDatamartMerchantTransactionHistory(DatamartHistory):
    class Meta:
        managed = False
        db_table = 'raw_datamart_merchant_transaction_history'

class RawDatamartPaymentTypeHistory(DatamartHistory):
    class Meta:
        managed = False
        db_table = 'raw_datamart_payment_type_history'

class DashboardReportStatus(models.Model):
    id_m_cms_menu = models.IntegerField()
    report_name = models.TextField()
    history_table_name = models.TextField()
    datamart_url = models.TextField()
    non_datamart_url = models.TextField()
    is_automate = models.BooleanField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'dashboard_report_status'


class ETLList(models.Model):
    id = models.AutoField(primary_key=True)
    etl_name = models.TextField()
    endpoint = models.TextField()
    is_active = models.BooleanField()
    is_running = models.BooleanField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'etl_list'
