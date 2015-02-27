# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('principal', '0013_auto_20150122_1455'),
    ]

    operations = [
        migrations.AddField(
            model_name='jugador',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, default=1, serialize=False, verbose_name='ID'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='jugador',
            name='nombre',
            field=models.CharField(unique=True, max_length=50),
        ),
    ]
