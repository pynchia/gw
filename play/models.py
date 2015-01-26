from django.db import models
from django.contrib.auth.models import User


# Limits
# max length of character's name
SUBJECT_NAME_MAX = 32

# max length of image filename (e.g. 01.png)
FILE_NAME_MAX = 6

# max length of feature's description
FEATURE_DESCR_MAX = 128

# the number of characters on each board
BOARD_ELEMENTS = 24


class Player(models.Model):
    """the player. Each player plays against the computer
    """
    user = models.OneToOneField(User)
    games_played = models.IntegerField(default=0)
    games_won = models.IntegerField(default=0)


class Game(models.Model):
    """"the games played by the player. Only one game can be active,
    The player must finish or cancel the current game before starting
    a new one.
    A game can be interrupted without any warning. It will resume
    automatically next time the player shows up 
    """
    player = models.ForeignKey(Player)
    active = models.BooleanField(default=True)
    won = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        get_latest_by = "created_on"


class Subject(models.Model):
    """the characters to be guessed
    """
    name = models.CharField(max_length=SUBJECT_NAME_MAX)
    filename = models.CharField(max_length=FILE_NAME_MAX)

    def __unicode__(self):
        return "%s (%s)" % (self.name, self.filename)


class Feature(models.Model):
    """the traits peculiar to each character
    (e.g. brown hair, wears glasses, gender, etc)
    """
    subject = models.ManyToManyField(Subject)
    description = models.CharField(max_length=FEATURE_DESCR_MAX)

    def __unicode__(self):
        return self.description


class BoardElement(models.Model):
    """The characters lying on the board (24 on the player's board and
    24 one the computer's)
    There will only be 24+24 entries for each player.
    They will be created when the player signs up.
    They refer to the latest game played. They will be recycled by
    every new game the player plays.
    """
    subject = models.ForeignKey(Subject)
    player = models.ForeignKey(Player)
    active = models.BooleanField(default=True)

