# -*- coding: utf-8 -*-
# Generated by Django 1.9.13 on 2019-05-23 10:07
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='course',
            name='detail',
        ),
    ]
