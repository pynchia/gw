# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('play', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='game',
            old_name='won',
            new_name='won_by_player',
        ),
        migrations.AddField(
            model_name='boardelement',
            name='owned_by_player',
            field=models.BooleanField(default=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='game',
            name='computer_subject',
            field=models.ForeignKey(related_name='computer_subj', default=1, to='play.Subject'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='game',
            name='player_subject',
            field=models.ForeignKey(related_name='player_subj', default=0, to='play.Subject'),
            preserve_default=False,
        ),
    ]
