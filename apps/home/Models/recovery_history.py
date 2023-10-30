from django.db import models


class RecoveryHistory(models.Model):
    ts_current = models.DateTimeField()
    id_user = models.BigIntegerField()
    id_cabang = models.BigIntegerField()
    num_row = models.TextField()
    time_process = models.FloatField()
    ts_end = models.DateTimeField()
    act_date = models.CharField(max_length = 32)

    class Meta:
        abstract = True

class RecoveryHistoryDatamartAkunting(RecoveryHistory):
    class Meta:
        managed = False
        db_table = 'recovery_history_datamart_akunting'

class RecoveryHistoryDatamartBusiestSellingTime(RecoveryHistory):
    class Meta:
        managed = False
        db_table = 'recovery_history_datamart_busiest_selling_time'

class RecoveryHistoryDatamartProduk(RecoveryHistory):
    class Meta:
        managed = False
        db_table = 'recovery_history_datamart_produk'

class RecoveryHistoryDatamartSubVarian(RecoveryHistory):
    class Meta:
        managed = False
        db_table = 'recovery_history_datamart_sub_varian'

class RecoveryHistoryDatamartVarian(RecoveryHistory):
    class Meta:
        managed = False
        db_table = 'recovery_history_datamart_varian'
### -----------------


##### VALIDATION HISTORIES
class ValidityHistory(models.Model):
    is_recovery = models.SmallIntegerField()
    id_user = models.BigIntegerField()
    id_cabang = models.BigIntegerField()
    data_target = models.IntegerField()
    data_source = models.IntegerField()
    status = models.CharField(max_length = 64)
    actdate = models.DateTimeField()
    ts_current = models.DateTimeField()
    ts_end = models.DateTimeField()

    class Meta:
        abstract = True

class ValidityHistoryAkunting(ValidityHistory):
    class Meta:
        managed = False
        db_table = 'validity_history_akunting'

class ValidityHistoryBusiestSellingTime(ValidityHistory):
    class Meta:
        managed = False
        db_table = 'validity_history_busiest_selling_time'

class ValidityHistoryProduk(ValidityHistory):
    class Meta:
        managed = False
        db_table = 'validity_history_produk'

class ValidityHistorySubVarian(ValidityHistory):
    class Meta:
        managed = False
        db_table = 'validity_history_sub_varian'

class ValidityHistoryVarian(ValidityHistory):
    class Meta:
        managed = False
        db_table = 'validity_history_varian'

class ValidityHistoryWaktuTeramai(ValidityHistory):
    class Meta:
        managed = False
        db_table = 'validity_history_waktu_teramai'

class ValidityHistoryCDC(models.Model):
    table_name = models.TextField()
    data_source = models.BigIntegerField()
    data_target = models.BigIntegerField()
    execution_time = models.FloatField()
    actdate = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'validity_history_cdc'

class TransactionsHistory(models.Model):
    id_transaction = models.BigIntegerField(primary_key=True)
    m_user_id_user = models.BigIntegerField()
    m_cabang_id_cabang = models.BigIntegerField()
    transaction_tgl = models.DateTimeField()
    updatedate = models.DateTimeField()
    createdate_datalake = models.DateTimeField()
    
    class Meta:
        managed = False
        db_table = 'transactions_history'

class RecoveryHistoryHardDelete(models.Model):
    id = models.BigIntegerField(primary_key=True)
    ts_current = models.DateTimeField()
    id_user = models.BigIntegerField()
    id_cabang = models.BigIntegerField()
    time_process = models.FloatField()
    actdate = models.DateTimeField()
    deleted_at = models.DateTimeField()
    params = models.TextField()
    
    class Meta:
        managed = False
        db_table = 'recovery_history_hard_delete'

class RecoveryHistoryPromo(models.Model):
    id = models.BigIntegerField(primary_key=True)
    m_user_id_user = models.BigIntegerField()
    m_cabang_id_cabang = models.BigIntegerField()
    transaction_tgl = models.DateField()
    createdate_datalake = models.DateTimeField()
    is_recovered_product = models.BooleanField()
    is_recovered_promo = models.BooleanField()
    is_recovered_compliment = models.BooleanField()
        
    class Meta:
        managed = False
        db_table = 'transaction_promo_history'
