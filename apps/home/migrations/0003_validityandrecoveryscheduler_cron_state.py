# Generated by Django 3.2.13 on 2022-11-09 16:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_auto_20221107_0948'),
    ]

    operations = [
        migrations.AddField(
            model_name='validityandrecoveryscheduler',
            name='cron_state',
            field=models.IntegerField(default=0),
        ),
    ]
