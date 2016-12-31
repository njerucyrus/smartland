# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='LandPurchasePayment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('transaction_id', models.CharField(unique=True, max_length=128, db_index=True)),
                ('title_deed', models.CharField(max_length=32)),
                ('purchased_size', models.FloatField()),
                ('payment_mode', models.CharField(max_length=20)),
                ('amount', models.FloatField()),
                ('status', models.CharField(max_length=32)),
                ('date', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name_plural': 'LandPurchasePayments',
            },
        ),
        migrations.CreateModel(
            name='LandTransferFee',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('land_size', models.FloatField()),
                ('fee_charged', models.FloatField()),
            ],
            options={
                'verbose_name_plural': 'LandTransferFee',
            },
        ),
        migrations.CreateModel(
            name='LandTransferPayment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('transaction_id', models.CharField(unique=True, max_length=128, db_index=True)),
                ('title_deed', models.CharField(max_length=32)),
                ('transferred_size', models.FloatField()),
                ('phone_number', models.CharField(max_length=13)),
                ('payment_mode', models.CharField(max_length=20)),
                ('amount', models.FloatField()),
                ('status', models.CharField(max_length=32)),
                ('date', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name_plural': 'LandTransferPayments',
            },
        ),
    ]
