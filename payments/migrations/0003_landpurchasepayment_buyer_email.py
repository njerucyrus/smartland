# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0002_auto_20161231_0914'),
    ]

    operations = [
        migrations.AddField(
            model_name='landpurchasepayment',
            name='buyer_email',
            field=models.EmailField(default='', max_length=254),
            preserve_default=False,
        ),
    ]
