# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('redsocial', '0004_auto_20150209_1452'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comentario',
            name='partida',
            field=models.ForeignKey(blank=True, to='principal.Partida', null=True),
        ),
    ]
