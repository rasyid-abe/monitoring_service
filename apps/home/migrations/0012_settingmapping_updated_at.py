# Generated by Django 3.2.13 on 2023-09-04 05:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0011_auto_20230904_1107'),
    ]

    operations = [
        migrations.AddField(
            model_name='settingmapping',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
