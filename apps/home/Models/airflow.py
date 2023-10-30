from django.db import models


class AirflowFailedTask(models.Model):
    task_id = models.CharField(max_length = 250)
    dag_id = models.CharField(max_length = 250)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    duration = models.IntegerField()
    map_index = models.IntegerField()
    run_id = models.CharField(max_length = 250)

    class Meta:
        managed = False
        db_table = 'task_fail'

class AirflowGeneralError(models.Model):
    timestamp = models.DateTimeField()
    filename = models.CharField(max_length = 250)
    stacktrace = models.TextField()

    class Meta:
        managed = False
        db_table = 'import_error'