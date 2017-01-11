# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('land', '0014_notification'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='read',
            field=models.BooleanField(default=False),
        ),
    ]
