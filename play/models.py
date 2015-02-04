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

    def matching_elements(self, player, owned_by_player):
        """Return the queryset of board elements matching
        the feature, player and belonging to the player/computer"""
        # get all the subjects matching the feature
        subjects = self.subject.all() 
        board_elements = player.boardelement_set.filter(
                                active=True,
                                owned_by_player=owned_by_player,
                                subject__in=subjects)
        return board_elements

    def __unicode__(self):
        return self.description


class Player(models.Model):
    """the player. Each player plays against the computer
    """
    # the django user it extends
    user = models.OneToOneField(User)
    # the number of games completed
    games_played = models.IntegerField(default=0)
    # the number of games won
    games_won = models.IntegerField(default=0)

    def add_board_elements(self):
        # create board element for the player
        for subj in Subject.objects.all():
            self.boardelement_set.create(player=self,
                                         subject=subj,
                                         owned_by_player=True)
        # and for the computer
        for subj in Subject.objects.all():
            self.boardelement_set.create(player=self,
                                         subject=subj,
                                         owned_by_player=False)

    def get_features(self, owned_by_player):
        """Return the features along with the number of board
        elements that match each"""
        features = Feature.objects.all()
        for feat in features:
            feat.num_el_match = feat.matching_elements(
                                    player=self,
                                    owned_by_player=owned_by_player).count()
        return features


class Game(models.Model):
    """"the games played by the player. Only one game can be active,
    The player must finish or cancel the current game before starting
    a new one.
    A game can be interrupted. It will resume automatically next time
    the player shows up
    """
    # to whom the game belongs
    player = models.ForeignKey(Player)
    # the subject the computer must guess
    player_subject = models.ForeignKey(Subject,
                                       related_name='player_subj')
    # the subject the player must guess
    computer_subject = models.ForeignKey(Subject,
                                         related_name='computer_subj')
    # if the game is pending
    active = models.BooleanField(default=True)
    # if the game was won by the player
    won_by_player = models.BooleanField(default=False)
    # timestamp
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        get_latest_by = "created_on"


class BoardElement(models.Model):
    """The characters lying on the board (24 on the player's board and
    24 on the computer's)
    There will only be 24+24 entries for each player.
    They will be created when the player signs up.
    They refer to the latest game played. They will be recycled by
    every new game the player plays.
    """
    subject = models.ForeignKey(Subject)
    player = models.ForeignKey(Player)
    active = models.BooleanField(default=True)
    owned_by_player = models.BooleanField(default=True)

    def __unicode__(self):
        return str(self.subject)
