# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('land', '0017_auto_20170106_1238'),
    ]

    operations = [
        migrations.AddField(
            model_name='landpurchases',
            name='approved',
            field=models.BooleanField(default=False),
        ),
    ]
