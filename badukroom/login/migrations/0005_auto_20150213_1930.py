# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0004_auto_20150122_1451'),
    ]

    operations = [
        migrations.AddField(
            model_name='perfil',
            name='path_portada',
            field=models.CharField(default=b'imagenes/None', max_length=70, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='perfil',
            name='path_principal',
            field=models.CharField(default=b'imagenes/None', max_length=70, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='perfil',
            name='fecha_nacimiento',
            field=models.DateField(help_text=b'Formato: dd/mm/yyyy'),
        ),
    ]
