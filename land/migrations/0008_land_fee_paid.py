# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('land', '0007_landpurchases'),
    ]

    operations = [
        migrations.AddField(
            model_name='land',
            name='fee_paid',
            field=models.BooleanField(default=False),
        ),
    ]
