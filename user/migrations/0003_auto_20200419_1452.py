# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2020-04-19 14:52
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_auto_20200419_1428'),
    ]

    operations = [
        migrations.AlterField(
            model_name='car',
            name='isout',
            field=models.CharField(default=0, max_length=2),
        ),
    ]