# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-04-04 12:16
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_poll_core', '0002_auto_20160330_1733'),
    ]

    operations = [
        migrations.AlterField(
            model_name='history_model',
            name='user',
            field=models.IntegerField(),
        ),
    ]
