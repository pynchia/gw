import random
from django.core.urlresolvers import reverse, reverse_lazy
from django.shortcuts import redirect
# from django.http import HttpResponseRedirect
from django.views import generic
# from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
# from django.contrib.auth.models import User

from play.models import Subject, BoardElement, Feature, Game


class NewGameView(generic.RedirectView):
    permanent = False
    pattern_name = "play:playgame"

    def get(self, request, difficulty):

        player = request.user.player

        # close any pending game
        player.game_set.filter(active=True).update(active=False)

        # create a new game
        subjects = Subject.objects.all()
        num_subjects = subjects.count()

        player_subject_id = random.randint(1, num_subjects)
        computer_subject_id = random.randint(1, num_subjects)
        player.game_set.create(player_subject_id=player_subject_id,
                               computer_subject_id=computer_subject_id,
                               difficulty=difficulty)
        
        # activate all board elements for the player
        player.boardelement_set.update(active=True)

        return super(NewGameView, self).get(request)


class PlayGameView(generic.ListView):
    template_name = "play/play.html"
    context_object_name = "player_board"

    def get_queryset(self):
        player = self.request.user.player
        return player.boardelement_set.filter(owned_by_player=True
                                             ).order_by('id')

    def get_context_data(self, **kwargs):
        context = super(PlayGameView, self).get_context_data(**kwargs)
        player = self.request.user.player
        context['player_features'] = player.get_features(
                                               owned_by_player=True)
        context['computer_board'] = BoardElement.objects.filter(
                                        player=player,
                                        owned_by_player=False).order_by('id')
        context['computer_features'] = player.get_features(
                                                 owned_by_player=False)
        context['game'] = player.game_set.latest()
        return context


class PickFeatureView(generic.TemplateView):
    template_name = "play/end.html"

#class PickFeatureView(generic.RedirectView):
    # Django bug 17914: reverse() and pattern_name give error
    # on namespaced views!
#    permanent = False
#    url = "/play/play"

    def get(self, request, feat_id):
        feature = Feature.objects.get(pk=feat_id)
        # all the characters who have that feature
        subjects = feature.subject.all()

        player = request.user.player
        game = player.game_set.filter(active=True).latest()
        match = game.computer_subject not in subjects 
        # get the characters onboard who do not match the feature
        elements = feature.matching_el(player=player,
                                       match=match,
                                       owned_by_player=True)
        # and deactivate them on the board
        elements.update(active=False)

        # now the computer moves
        # how many characters remain on player's board
        player_num_el = player.board_el(owned_by_player=True).count()
        # how many characters are on computer's board
        computer_num_el = player.board_el(owned_by_player=False).count()
        if player_num_el > 1 or computer_num_el == 2:
            if computer_num_el == 2:
                if player_num_el == 1:
                    game.won_by = game.DRAW
                else:
                    game.won_by = game.COMPUTER
            else:
                # pick the best feature according to the difficulty
                feature = game.pick_best_feature(computer_num_el)
                # all the characters who have that feature
                subjects = feature.subject.all()
                match = game.player_subject not in subjects 
                # get the characters onboard who do not match the feature
                elements = feature.matching_el(player=player,
                                               match=match,
                                               owned_by_player=False)
                # and deactivate them on the board
                elements.update(active=False)
                computer_num_el = player.board_el(owned_by_player=False
                                                 ).count()
                if computer_num_el == 1:
                    game.won_by = game.COMPUTER
                else:
                    # go ahead to the player's turn
                    return redirect(reverse_lazy("play:playgame"))
        else:
            # it must guess the player's character
            # get the remaining characters on its board
            computer_els = player.board_el(owned_by_player=False)
            # guess one randomly
            guessed_el = random.choice(computer_els)
            # is it the correct guess?
            if guessed_el.subject == game.player_subject:
                # yes! It's a DRAW!
                game.won_by = game.DRAW
            else:
                game.won_by = game.PLAYER

        game.active = False
        game.save()
        self.game = game

        return super(PickFeatureView, self).get(request)

    def get_context_data(self, **kwargs):
        context = super(PickFeatureView, self).get_context_data(**kwargs)
        context['game'] = self.game
        return context


