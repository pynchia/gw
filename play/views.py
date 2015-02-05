from django.core.urlresolvers import reverse_lazy
# from django.http import HttpResponseRedirect
from django.views import generic
# from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

from play.models import BoardElement, Player, Feature


class NewGameView(generic.RedirectView):
    pattern_name = "play"

    def get(self, request, *args, **kwargs):

        # close any pending game

        # create a new game
        # activate all board elements

        return super(NewGameView, self).get(request, *args, **kwargs)


class PlayGameView(generic.ListView):
    template_name = "play/play.html"
    context_object_name = "player_board"

    def get_queryset(self):
        return BoardElement.objects.filter(
                player=self.request.user.player,
                owned_by_player=True).order_by('id')

    def get_context_data(self):
        context = super(PlayGameView, self).get_context_data()
        context['player_features'] = self.request.user.player.get_features(
                                                       owned_by_player=True)
        context['computer_board'] = BoardElement.objects.filter(
                                        player=self.request.user.player,
                                        owned_by_player=False).order_by('id')
        context['computer_features'] = self.request.user.player.get_features(
                                                       owned_by_player=False)
        context['game'] = self.request.user.player.game_set.latest()
        return context

