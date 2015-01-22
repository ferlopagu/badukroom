# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('principal', '0005_auto_20150116_1526'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='jugador',
            name='id',
        ),
        migrations.AlterField(
            model_name='jugador',
            name='nombre',
            field=models.CharField(max_length=50, serialize=False, primary_key=True),
        ),
        migrations.AlterField(
            model_name='partida',
            name='fichero',
            field=models.FileField(upload_to=b'/home/fla2727/workspace/tfg/badukroom/static/sgf'),
        ),
    ]
