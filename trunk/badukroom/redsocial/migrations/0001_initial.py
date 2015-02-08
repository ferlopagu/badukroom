# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0004_auto_20150122_1451'),
        ('principal', '0013_auto_20150122_1455'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comentario',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('fecha', models.DateTimeField()),
                ('texto', models.CharField(max_length=2000)),
                ('fichero', models.FileField(upload_to=b'/home/fla2727/workspace/tfg/badukroom/static/sgf')),
                ('partida', models.ForeignKey(to='principal.Partida')),
                ('perfil', models.ForeignKey(to='login.Perfil')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Notificacion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('mensaje', models.CharField(max_length=300)),
                ('receptor', models.ForeignKey(to='login.Perfil')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PeticionAmistad',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('es_aceptada', models.BooleanField(default=False)),
                ('es_rechazada', models.BooleanField(default=False)),
                ('emisor', models.ForeignKey(related_name=b'sender', to='login.Perfil')),
                ('receptor', models.ForeignKey(related_name=b'receiver', to='login.Perfil')),
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
