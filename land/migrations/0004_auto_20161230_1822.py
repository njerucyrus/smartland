# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('land', '0003_auto_20161230_1757'),
    ]

    operations = [
        migrations.AlterField(
            model_name='landtransfers',
            name='new_title_deed',
            field=models.CharField(unique=True, max_length=32),
        ),
    ]
