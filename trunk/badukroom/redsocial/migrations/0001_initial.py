# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0004_auto_20150122_1451'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comentario',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('fecha', models.DateTimeField()),
                ('texto', models.CharField(max_length=2000)),
                ('fichero', models.FileField(upload_to=b'/home/fla2727/workspace/tfg/badukroom/static/sgf', blank=True)),
                ('perfil', models.ForeignKey(to='login.Perfil')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Respuesta',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('fecha', models.DateTimeField()),
                ('texto', models.CharField(max_length=2000)),
                ('fichero', models.FileField(upload_to=b'/home/fla2727/workspace/tfg/badukroom/static/sgf', blank=True)),
                ('comentario', models.ForeignKey(to='redsocial.Comentario')),
                ('perfil', models.ForeignKey(to='login.Perfil')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
