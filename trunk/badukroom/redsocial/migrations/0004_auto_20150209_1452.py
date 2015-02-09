# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('redsocial', '0003_comentario_grupo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comentario',
            name='grupo',
            field=models.ForeignKey(blank=True, to='redsocial.Grupo', null=True),
        ),
        migrations.AlterField(
            model_name='comentario',
            name='partida',
            field=models.ForeignKey(to='principal.Partida', blank=True),
        ),
    ]
