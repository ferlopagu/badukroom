# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Jugador',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre', models.CharField(unique=True, max_length=50)),
                ('es_profesional', models.BooleanField(default=False)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Partida',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('fecha', models.DateField()),
                ('rango_negro', models.CharField(max_length=50)),
                ('rango_blanco', models.CharField(max_length=50)),
                ('resultado', models.CharField(max_length=50)),
                ('fichero', models.FileField(upload_to=b'partida')),
                ('path', models.CharField(max_length=70, blank=True)),
                ('es_profesional', models.BooleanField(default=False)),
                ('sgf_size', models.IntegerField(default=0)),
                ('jugador_blanco', models.ForeignKey(related_name=b'Jugador_jugador_blanco', to='principal.Jugador')),
                ('jugador_negro', models.ForeignKey(related_name=b'Jugador_jugador_negro', to='principal.Jugador')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Revisor',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nickname_kgs', models.CharField(unique=True, max_length=20)),
                ('perfil', models.OneToOneField(to='login.Perfil')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Sgf',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('fecha', models.DateField()),
                ('jugador_negro', models.CharField(max_length=100)),
                ('jugador_blanco', models.CharField(max_length=100)),
                ('fichero', models.FileField(upload_to=b'sgf')),
                ('path', models.CharField(max_length=70, blank=True)),
                ('sgf_size', models.IntegerField(default=0)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='sgf',
            unique_together=set([('jugador_negro', 'jugador_blanco', 'fecha', 'sgf_size')]),
        ),
        migrations.AddField(
            model_name='partida',
            name='revisor',
            field=models.ForeignKey(blank=True, to='principal.Revisor', null=True),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='partida',
            unique_together=set([('jugador_negro', 'jugador_blanco', 'fecha', 'sgf_size')]),
        ),
    ]
