# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0003_auto_20150122_1412'),
    ]

    operations = [
        migrations.AlterField(
            model_name='perfil',
            name='foto_portada',
            field=models.ImageField(upload_to=b'/home/fla2727/workspace/tfg/badukroom/static/imagenes', blank=True),
        ),
        migrations.AlterField(
            model_name='perfil',
            name='foto_principal',
            field=models.ImageField(upload_to=b'/home/fla2727/workspace/tfg/badukroom/static/imagenes', blank=True),
        ),
    ]
