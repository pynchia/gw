"""Custom signal receivers
"""
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from .models import Player


@receiver(post_save, sender=User)
def create_player(sender, instance, created, **kwargs):
    if created:
        player = Player()
        player.user = instance
        player.save()
        player.add_board_elements()
