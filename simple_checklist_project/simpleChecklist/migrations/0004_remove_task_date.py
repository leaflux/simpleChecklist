# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-05-25 00:30
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('simpleChecklist', '0003_task_slug'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='task',
            name='date',
        ),
    ]