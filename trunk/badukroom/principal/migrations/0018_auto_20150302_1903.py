# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('principal', '0017_auto_20150226_1212'),
    ]

    operations = [
        migrations.AddField(
            model_name='partida',
            name='sgf_size',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='partida',
            unique_together=set([('jugador_negro', 'jugador_blanco', 'fecha', 'sgf_size')]),
        ),
    ]
