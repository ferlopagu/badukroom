# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('principal', '0011_auto_20150122_1428'),
    ]

    operations = [
        migrations.AlterField(
            model_name='partida',
            name='fichero',
            field=models.FileField(upload_to=b'/home/fla2727/workspace/tfg/badukroom/static/'),
        ),
    ]