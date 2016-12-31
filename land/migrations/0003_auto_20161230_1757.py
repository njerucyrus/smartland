# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('land', '0002_auto_20161228_0857'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='landtransfers',
            name='transferred_to',
        ),
        migrations.AddField(
            model_name='land',
            name='map_sheet',
            field=models.CharField(default='', max_length=32),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='landtransfers',
            name='transfer_to',
            field=models.CharField(default='', max_length=32, verbose_name=b'Transfer To (Username)'),
            preserve_default=False,
        ),
    ]
