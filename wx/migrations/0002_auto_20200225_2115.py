# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2020-02-25 21:15
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wx', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='password',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='phone',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='updated_time',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='username',
        ),
        migrations.AddField(
            model_name='userprofile',
            name='isStop',
            field=models.CharField(default=False, max_length=5),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='email',
            field=models.EmailField(max_length=254, null=True),
        ),
    ]
