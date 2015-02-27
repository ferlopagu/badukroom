# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0008_auto_20150220_1941'),
        ('principal', '0014_auto_20150225_1624'),
    ]

    operations = [
        migrations.CreateModel(
            name='Revisor',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nickname_kgs', models.CharField(max_length=20)),
                ('perfil', models.ForeignKey(to='login.Perfil')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='partida',
            name='revisor',
            field=models.ForeignKey(blank=True, to='principal.Revisor', null=True),
            preserve_default=True,
        ),
    ]
