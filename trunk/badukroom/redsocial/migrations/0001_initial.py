# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('principal', '0001_initial'),
        ('login', '0002_auto_20150530_2126'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comentario',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('fecha', models.DateTimeField()),
                ('texto', models.TextField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Grupo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('titulo', models.CharField(max_length=300)),
                ('descripcion', models.TextField(max_length=600)),
                ('foto_portada', models.ImageField(default=b'imagenes/sin_portada.jpg', upload_to=b'imagenes', blank=True)),
                ('path_portada', models.CharField(default=b'imagenes/sin_portada.jpg', max_length=70, blank=True)),
                ('miembros', models.ManyToManyField(to='login.Perfil')),
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
                ('revision', models.BooleanField(default=False)),
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
            name='PeticionRevision',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('mensaje', models.CharField(max_length=300)),
                ('revision', models.BooleanField(default=False)),
                ('partida_id', models.IntegerField()),
                ('emisor', models.ForeignKey(related_name=b'sender1', to='login.Perfil')),
                ('receptor', models.ForeignKey(related_name=b'receiver1', to='login.Perfil')),
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
                ('comentario', models.ForeignKey(to='redsocial.Comentario')),
                ('partida', models.ForeignKey(blank=True, to='principal.Sgf', null=True)),
                ('perfil', models.ForeignKey(to='login.Perfil')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='comentario',
            name='grupo',
            field=models.ForeignKey(blank=True, to='redsocial.Grupo', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='comentario',
            name='partida',
            field=models.ForeignKey(blank=True, to='principal.Sgf', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='comentario',
            name='perfil',
            field=models.ForeignKey(to='login.Perfil'),
            preserve_default=True,
        ),
    ]
