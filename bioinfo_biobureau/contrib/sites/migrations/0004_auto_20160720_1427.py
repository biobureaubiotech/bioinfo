# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-20 14:27
from __future__ import unicode_literals

import django.contrib.sites.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sites', '0003_auto_20160720_1111'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='site',
            managers=[
                ('objects', django.contrib.sites.models.SiteManager()),
            ],
        ),
    ]
