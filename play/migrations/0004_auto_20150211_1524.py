# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('play', '0003_auto_20150209_1015'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='game',
            name='won_by_player',
        ),
        migrations.RemoveField(
            model_name='player',
            name='games_played',
        ),
        migrations.RemoveField(
            model_name='player',
            name='games_won',
        ),
        migrations.AddField(
            model_name='game',
            name='won_by',
            field=models.IntegerField(default=0, choices=[(0, b'Draw'), (1, b'Player'), (2, b'Computer')]),
            preserve_default=True,
        ),
    ]
