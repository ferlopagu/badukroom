# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('redsocial', '0002_auto_20150209_1409'),
    ]

    operations = [
        migrations.AddField(
            model_name='comentario',
            name='grupo',
            field=models.ForeignKey(to='redsocial.Grupo', null=True),
            preserve_default=True,
        ),
    ]
