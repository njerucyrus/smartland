# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('land', '0018_landpurchases_approved'),
    ]

    operations = [
        migrations.AddField(
            model_name='landpurchases',
            name='rejected',
            field=models.BooleanField(default=False),
        ),
    ]
