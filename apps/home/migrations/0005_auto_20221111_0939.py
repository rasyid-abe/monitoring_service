# Generated by Django 3.2.13 on 2022-11-11 02:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0004_auto_20221111_0937'),
    ]

    operations = [
        migrations.AlterField(
            model_name='validityandrecoveryscheduler',
            name='end_at',
            field=models.TimeField(),
        ),
        migrations.AlterField(
            model_name='validityandrecoveryscheduler',
            name='start_at',
            field=models.TimeField(),
        ),
    ]
