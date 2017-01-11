# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('land', '0019_landpurchases_rejected'),
    ]

    operations = [
        migrations.AlterField(
            model_name='landpurchases',
            name='land',
            field=models.OneToOneField(to='land.Land'),
        ),
    ]
