# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-03-30 12:03
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_poll_core', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answer_model',
            name='vote',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='poll_model',
            name='total_vote',
            field=models.IntegerField(default=0),
        ),
    ]