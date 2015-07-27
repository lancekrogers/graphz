# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('awesome', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='graph',
            name='data',
            field=models.TextField(db_index=True, default=''),
            preserve_default=False,
        ),
    ]
