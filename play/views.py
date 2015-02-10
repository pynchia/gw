from random import randint
# from django.core.urlresolvers import reverse, reverse_lazy
# from django.http import HttpResponseRedirect
from django.views import generic
# from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
# from django.contrib.auth.models import User

from play.models import Subject, BoardElement, Feature, Game


class NewGameView(generic.RedirectView):
    permanent = False
    pattern_name = "play:playgame"

    def get(self, request, *args, **kwargs):

        player = request.user.player

        # close any pending game
        # player.game_set.filter(active=True).update(active=False)

        # create a new game
        subjects = Subject.objects.all()
        num_subjects = subjects.count()

        player_subject = subjects[randint(0, num_subjects-1)]
        computer_subject = subjects[randint(0, num_subjects-1)]
        game = Game(player=player, computer_subject=computer_subject,
                    player_subject=player_subject)
        game.save()
        #player.game_set.add(game)
        #player.game_set.create(player_subject_id=player_subject_id,
        #                       computer_subject_id=computer_subject_id)
        
        # activate all board elements for the player
        player.boardelement_set.update(active=True)

        return super(NewGameView, self).get(request, *args, **kwargs)


class PlayGameView(generic.ListView):
    template_name = "play/play.html"
    context_object_name = "player_board"

    def get_queryset(self):
        player = self.request.user.player
        return player.boardelement_set.filter(owned_by_player=True
                                             ).order_by('id')

    def get_context_data(self):
        player = self.request.user.player
        context = super(PlayGameView, self).get_context_data()
        context['player_features'] = player.get_features(
                                               owned_by_player=True)
        context['computer_board'] = BoardElement.objects.filter(
                                        player=player,
                                        owned_by_player=False).order_by('id')
        context['computer_features'] = player.get_features(
                                                 owned_by_player=False)
        context['game'] = player.game_set.latest()
        return context


class PickFeatureView(generic.RedirectView):
    # Django bug 17914: reverse() and pattern_name give error
    # on namespaced views!
    permanent = False
    url = "/play/play"

    def get(self, request, *args, **kwargs):
        feat_id = kwargs['feat_id']
        feature = Feature.objects.get(pk=feat_id)
        # all the characters who have that feature
        subjects = feature.subject.all()

        player = request.user.player
        game = player.game_set.filter(active=True).latest()
        match = game.computer_subject not in subjects 
        elements = feature.matching_el(player=player,
                                       match=match,
                                       owned_by_player=True)
        elements.update(active=False)

        num_el_left = player.board_el(owned_by_player=True).count()
        if num_el_left == 1:  # only one left! Winner!
            game.won_by_player = True
            game.active = False
            game.save()

        return super(PickFeatureView, self).get(request, *args, **kwargs)

