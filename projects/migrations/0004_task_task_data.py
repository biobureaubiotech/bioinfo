# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-08-08 16:35
from __future__ import unicode_literals

import django.contrib.postgres.fields.jsonb
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0003_task'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='task_data',
            field=django.contrib.postgres.fields.jsonb.JSONField(default=1),
            preserve_default=False,
        ),
    ]
