# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-02-27 08:50
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app_poll_core', '0004_auto_20160227_1419'),
    ]

    operations = [
        migrations.RenameField(
            model_name='pollanswer',
            old_name='question',
            new_name='question_id',
        ),
        migrations.RenameField(
            model_name='pollhistory',
            old_name='answer',
            new_name='answer_id',
        ),
        migrations.RenameField(
            model_name='pollhistory',
            old_name='question',
            new_name='question_id',
        ),
    ]