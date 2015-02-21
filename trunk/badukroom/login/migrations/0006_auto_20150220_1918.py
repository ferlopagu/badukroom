# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0005_auto_20150213_1930'),
    ]

    operations = [
        migrations.AlterField(
            model_name='perfil',
            name='foto_portada',
            field=models.ImageField(default=b'/home/fla2727/workspace/tfg/badukroom/static//imagenes/sin_portada.jpg', upload_to=b'/home/fla2727/workspace/tfg/badukroom/static/imagenes', blank=True),
        ),
        migrations.AlterField(
            model_name='perfil',
            name='foto_principal',
            field=models.ImageField(default=b'/home/fla2727/workspace/tfg/badukroom/static//imagenes/sin_foto.jpg', upload_to=b'/home/fla2727/workspace/tfg/badukroom/static/imagenes', blank=True),
        ),
        migrations.AlterField(
            model_name='perfil',
            name='path_portada',
            field=models.FilePathField(path=b'/home/fla2727/workspace/tfg/badukroom/static/imagenes'),
        ),
        migrations.AlterField(
            model_name='perfil',
            name='path_principal',
            field=models.FilePathField(path=b'/home/fla2727/workspace/tfg/badukroom/static/imagenes'),
        ),
    ]
