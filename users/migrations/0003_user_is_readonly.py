# Generated by Django 3.2.13 on 2022-12-27 01:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20221220_2321'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_readonly',
            field=models.BooleanField(default=True),
        ),
    ]
