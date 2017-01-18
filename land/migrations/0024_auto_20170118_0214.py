# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-01-18 02:14
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('land', '0023_auto_20170118_0210'),
    ]

    operations = [
        migrations.AlterField(
            model_name='land',
            name='land_value',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name=b'Land Value (Ksh)'),
        ),
    ]
