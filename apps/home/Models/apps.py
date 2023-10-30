from django.db import models

class ValidityAndRecoveryScheduler(models.Model):
    id = models.BigAutoField(primary_key=True)
    etl_name = models.CharField(max_length = 100)
    recovery_name = models.CharField(max_length = 100)
    start_at = models.TimeField()
    end_at = models.TimeField()
    cron_state = models.SmallIntegerField(default=0)
    created_at = models.DateTimeField()

    class Meta:
        db_table = 'home_validity_recovery_scheduler'


class Alert(models.Model):
    id = models.BigAutoField(primary_key=True)
    alert_name = models.CharField(max_length = 100)
    status = models.SmallIntegerField(default=0)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        db_table = 'home_alert'

class AlertDetail(models.Model):
    id = models.BigAutoField(primary_key=True)
    id_alert = models.ForeignKey("Alert", on_delete=models.CASCADE)
    alert_detail_name = models.CharField(max_length = 100)
    status = models.SmallIntegerField(default=0)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    detail = models.JSONField(default=None, null=True)

    class Meta:
        db_table = 'home_alert_detail'

class AlertHistory(models.Model):
    id = models.BigAutoField(primary_key=True)
    id_alert_detail = models.ForeignKey("AlertDetail", on_delete=models.CASCADE)
    type = models.SmallIntegerField(default=1)
    message = models.TextField()
    created_at = models.DateTimeField()

    class Meta:
        db_table = 'home_alert_history'

class RecoveryMapping(models.Model):
    id = models.BigAutoField(primary_key=True)
    etl_name = models.CharField(max_length=100)
    url = models.CharField(max_length=255)

    class Meta:
        db_table = 'home_validity_recovery_mapping'


class SettingMapping(models.Model):
    id = models.BigAutoField(primary_key=True)
    setting_name = models.CharField(max_length=100)
    value = models.JSONField(default=None, null=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'home_setting_mapping'
