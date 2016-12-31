# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='landtransferpayment',
            name='status',
            field=models.CharField(default=b'PendingConfirmation', max_length=32),
        ),
    ]
