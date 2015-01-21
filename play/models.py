from django.db import models
from django.contrib.auth.models import User


SUBJECT_NAME = 32
FEATURE_DESCR = 128


class Player(models.Model):
    user = models.OneToOneField(User)
    games_played = models.IntegerField(default=0)
    games_won = models.IntegerField(default=0)


class Game(models.Model):
    player = models.ForeignKey(Player)
    created_on = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)


class Subject(models.Model):
    name = models.CharField(max_length=SUBJECT_NAME)


class Feature(models.Model):
    subject = models.ManyToManyField(Subject)
    description = models.CharField(max_length=FEATURE_DESCR)


class BoardElement(models.Model):
    subject = models.ForeignKey(Subject)


