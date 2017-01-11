# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('land', '0020_auto_20170107_0543'),
    ]

    operations = [
        migrations.AddField(
            model_name='land',
            name='purchased',
            field=models.BooleanField(default=True),
        ),
    ]
