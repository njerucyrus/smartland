# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('land', '0012_auto_20170102_0938'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='land',
            options={'ordering': ('-date_registered',), 'verbose_name_plural': 'Lands'},
        ),
        migrations.AlterModelOptions(
            name='landpurchases',
            options={'ordering': ('-date',), 'verbose_name_plural': 'LandPurchases'},
        ),
        migrations.AlterModelOptions(
            name='landtransfers',
            options={'ordering': ('-date_transferred',), 'verbose_name_plural': 'LandTransfers'},
        ),
        migrations.AddField(
            model_name='land',
            name='date_registered',
            field=models.DateTimeField(default=datetime.datetime(2017, 1, 2, 9, 42, 11, 202701, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
    ]
