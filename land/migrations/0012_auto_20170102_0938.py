# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('land', '0011_auto_20170102_0936'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='contactus',
            options={'ordering': ('-date',), 'verbose_name_plural': 'ContactUs Messages'},
        ),
        migrations.AddField(
            model_name='contactus',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2017, 1, 2, 9, 38, 27, 442276, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
    ]
