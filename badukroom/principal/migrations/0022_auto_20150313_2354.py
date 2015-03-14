# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('principal', '0021_partidarepositorio'),
    ]

    operations = [
        migrations.AlterField(
            model_name='partidarepositorio',
            name='es_profesional',
            field=models.BooleanField(default=False),
        ),
    ]
