# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0008_auto_20150220_1941'),
        ('redsocial', '0009_peticionrevision'),
    ]

    operations = [
        migrations.CreateModel(
            name='Mensaje',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('mensaje', models.CharField(max_length=300)),
                ('fecha', models.DateTimeField()),
                ('emisor', models.ForeignKey(related_name=b'emisorMensaje', to='login.Perfil')),
                ('receptor', models.ForeignKey(related_name=b'receptorMensaje', to='login.Perfil')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
