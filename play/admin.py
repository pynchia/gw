from django.contrib import admin
from .models import Player, Game, Subject, Feature, BoardElement


# Register your models here.
admin.site.register(Player)
admin.site.register(Game)
admin.site.register(Subject)
admin.site.register(Feature)
admin.site.register(BoardElement)

