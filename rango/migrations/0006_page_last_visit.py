# Generated by Django 3.1.4 on 2021-01-10 22:34

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('rango', '0005_userprofile'),
    ]

    operations = [
        migrations.AddField(
            model_name='page',
            name='last_visit',
            field=models.DateTimeField(default=datetime.datetime(2021, 1, 10, 22, 34, 33, 843608, tzinfo=utc)),
        ),
    ]