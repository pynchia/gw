import random
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

class _FeatureMgr(models.Manager):

    def get_features(self, player, owned_by_player, all_features):
        """Given a player and a board (player's or computer's)
        return the features along with the number of board elements
        (characters) that match each.
        Those features present in the whole set of board elements or
        in none of them are returned only if the all_features flag is True
        """
        # get all the possible features
        # TBD it should work if
        features = self.all()
        # features = Feature.objects.all()
        num_el_onboard = BoardElement.objects.board_el(player=player,
                                            owned_by_player=owned_by_player
                                            ).count()
        feat_list = []
        for feat in features:
            num_el_match = BoardElement.objects.matching_el(feature=feat,
                                                            player=player,
                                                            match=True,
                                            owned_by_player=owned_by_player
                                           ).count()
            if all_features or \
               (num_el_match != 0 and num_el_match != num_el_onboard):
                feat.num_el_match = num_el_match
                feat_list.append(feat)

        feat_list.sort(key=lambda f: f.num_el_match, reverse=True)
        return feat_list

    def pick_best_feature(self, game, computer_num_el):
        """Find the best feature to pick (for the computer), based
        on the difficulty of the game"""
        features = Feature.objects.get_features(player=game.player,
                                                owned_by_player=False,
                                                all_features=False)
        if game.difficulty == game.EASY:
            # pick a feature at random
            best_feature = random.choice(features)
        else:
            # pick the most probable feature
            computer_num_el /= 2
            for best_feature in features:
                if best_feature.num_el_match <= computer_num_el:
                    break
        return best_feature


class Feature(models.Model):
    """the traits peculiar to each character
    (e.g. brown hair, wears glasses, gender, etc)
    """
    subject = models.ManyToManyField(Subject)
    description = models.CharField(max_length=FEATURE_DESCR_MAX)

    objects = _FeatureMgr()

    def __unicode__(self):
        return self.description


class Player(models.Model):
    """the player. Each player plays against the computer
    """
    # the django user it extends
    user = models.OneToOneField(User)

    # add any further attributes beloging to the player

    def __unicode__(self):
        return self.user


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
                                       related_name='player_subject')
    # the subject the player must guess
    computer_subject = models.ForeignKey(Subject,
                                         related_name='computer_subject')
    # if the game is pending
    active = models.BooleanField(default=True)

    # who won the game
    DRAW = 0
    PLAYER = 1
    COMPUTER = 2
    WON_BY_CHOICES = (
            (DRAW, "Draw"),
            (PLAYER, "Player"),
            (COMPUTER, "Computer"),
    )
    won_by = models.IntegerField(choices=WON_BY_CHOICES, default=DRAW)

    # the level at which the computer plays
    EASY = 0
    HARD = 1
    DIFFICULTY_CHOICES = (
            (EASY, "Easy"),
            (HARD, "Hard"),
    )
    difficulty = models.IntegerField(choices=DIFFICULTY_CHOICES,
                                     default=EASY)

    # timestamp
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        get_latest_by = "created_on"

    def __unicode__(self):
        return u"player=%s, player_subject=%s, computer_subject=%s, active=%s, won by=%s, difficulty=%s" % (self.player.user, self.player_subject,
                              self.computer_subject, self.active,
                              self.get_won_by_display(),
                              self.get_difficulty_display())


class _BoardElementMgr(models.Manager):

    def add_board_elements(self, player):
        """Create all the board elements for the given player.
        Each player has two sets of characters: one set for the ones in
        the player's board and one set for the ones in the computer's
        board. The two sets are reused by each new game
        """
        # create the board elements in the player's board
        for subj in Subject.objects.all():
            player.boardelement_set.create(subject=subj,
                                         owned_by_player=True)
        # create the board elements in the computer's board
        for subj in Subject.objects.all():
            player.boardelement_set.create(subject=subj,
                                         owned_by_player=False)

    def board_el(self, player, owned_by_player):
        """Return the player's active board elements
        belonging to the player/computer"""
        return player.boardelement_set.filter(
                                        active=True,
                                        owned_by_player=owned_by_player)

    def matching_el(self, feature, player, match, owned_by_player):
        """Return the player's active board elements matching/non-matching
        (match=True/match=False) the feature and belonging to the
        player/computer"""
        # all the characters who have that feature
        subjects = feature.subject.all() 
        # get all the characters on the board
        board_elements = self.board_el(player=player,
                                       owned_by_player=owned_by_player)
        if match:
            # get all the characters on the board matching the feature
            match_elements = board_elements.filter(subject__in=subjects)
        else:
            # get all the characters on the board non-matching the feature
            match_elements = board_elements.exclude(subject__in=subjects)
        return match_elements


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

    objects = _BoardElementMgr()

    def __unicode__(self):
        return str(self.subject)
