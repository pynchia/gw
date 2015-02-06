from django.core.urlresolvers import reverse_lazy
# from django.http import HttpResponseRedirect
from django.views import generic
# from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

from play.models import BoardElement, Player, Feature


class NewGameView(generic.RedirectView):
    pattern_name = "play:playgame"

    def get(self, request, *args, **kwargs):

        # close any pending game
        player = self.request.user.player
        player.game_set.filter(active=True).update(active=False)

        # create a new game
        player_subject_id = 1
        computer_subject_id = 2
        player.game_set.create(player_subject_id=player_subject_id,
                               computer_subject_id=computer_subject_id)
        
        # activate all board elements for the player
        player.boardelement_set.update(active=True)

        return super(NewGameView, self).get(request, *args, **kwargs)


class PlayGameView(generic.ListView):
    template_name = "play/play.html"
    context_object_name = "player_board"

    def get_queryset(self):
        return BoardElement.objects.filter(
                player=self.request.user.player,
                owned_by_player=True).order_by('id')

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

