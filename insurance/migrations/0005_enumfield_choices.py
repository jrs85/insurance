# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2018-12-04 00:04
from __future__ import unicode_literals

from django.db import migrations
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('insurance', '0004_enumfield_enumvalue'),
    ]

    operations = [
        migrations.AddField(
            model_name='enumfield',
            name='choices',
            field=jsonfield.fields.JSONField(default=dict),
        ),
    ]
