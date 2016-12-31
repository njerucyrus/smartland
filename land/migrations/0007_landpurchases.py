# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('land', '0006_auto_20161231_1855'),
    ]

    operations = [
        migrations.CreateModel(
            name='LandPurchases',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('deposit', models.DecimalField(default=0.0, max_digits=10, decimal_places=2)),
                ('phone_number', models.CharField(max_length=13)),
                ('email', models.EmailField(max_length=254)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('buyer', models.ForeignKey(to='land.LandUserProfile')),
                ('land', models.ForeignKey(to='land.Land')),
            ],
            options={
                'verbose_name_plural': 'LandPurchases',
            },
        ),
    ]
