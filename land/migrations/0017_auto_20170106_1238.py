# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('land', '0016_contactus_phone_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contactus',
            name='phone_number',
            field=models.CharField(max_length=13, null=True, blank=True),
        ),
    ]
