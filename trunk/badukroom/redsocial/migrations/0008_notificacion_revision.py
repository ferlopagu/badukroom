# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('redsocial', '0007_auto_20150223_1511'),
    ]

    operations = [
        migrations.AddField(
            model_name='notificacion',
            name='revision',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
