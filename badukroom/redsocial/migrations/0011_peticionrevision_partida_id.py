# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('redsocial', '0010_mensaje'),
    ]

    operations = [
        migrations.AddField(
            model_name='peticionrevision',
            name='partida_id',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]
