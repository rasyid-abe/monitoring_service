# Generated by Django 3.2.13 on 2023-01-10 08:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0005_auto_20221111_0939'),
    ]

    operations = [
        migrations.CreateModel(
            name='AirflowFailedTask',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('task_id', models.CharField(max_length=250)),
                ('dag_id', models.CharField(max_length=250)),
                ('start_date', models.DateTimeField()),
                ('end_date', models.DateTimeField()),
                ('duration', models.IntegerField()),
                ('map_index', models.IntegerField()),
                ('run_id', models.CharField(max_length=250)),
            ],
            options={
                'db_table': 'task_fail',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='AirflowGeneralError',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField()),
                ('filename', models.CharField(max_length=250)),
                ('stacktrace', models.TextField()),
            ],
            options={
                'db_table': 'import_error',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='RawDatamartProductHistory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('actdate', models.DateTimeField()),
                ('ts_current', models.DateTimeField()),
                ('ts_end', models.DateTimeField()),
                ('num_row', models.IntegerField()),
                ('time_process', models.FloatField()),
                ('params', models.TextField()),
            ],
            options={
                'db_table': 'raw_datamart_product_history',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Alert',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('alert_name', models.CharField(max_length=100)),
                ('status', models.SmallIntegerField(default=0)),
                ('created_at', models.DateTimeField()),
                ('updated_at', models.DateTimeField()),
            ],
            options={
                'db_table': 'home_alert',
            },
        ),
        migrations.CreateModel(
            name='AlertDetail',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('alert_detail_name', models.CharField(max_length=100)),
                ('status', models.SmallIntegerField(default=0)),
                ('created_at', models.DateTimeField()),
                ('updated_at', models.DateTimeField()),
                ('id_alert', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.alert')),
            ],
            options={
                'db_table': 'home_alert_detail',
            },
        ),
        migrations.CreateModel(
            name='AlertHistory',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('type', models.SmallIntegerField(default=1)),
                ('message', models.TextField()),
                ('created_at', models.DateTimeField()),
                ('id_alert_detail', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.alertdetail')),
            ],
            options={
                'db_table': 'home_alert_history',
            },
        ),
    ]
