from django.core.urlresolvers import reverse_lazy
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect
from django.views import generic
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

from django.db.models import Count
from play.models import Player, Game


class SignUpView(generic.CreateView):
    model = User
    template_name = "accounts/signup.html"
    form_class = UserCreationForm
    success_url = reverse_lazy("login")


class LoginView(generic.FormView):
    template_name = "accounts/login.html"
    form_class = AuthenticationForm
    success_url = reverse_lazy("home")

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            return HttpResponseRedirect(self.get_success_url())
        else:
            return super(LoginView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        login(self.request, form.get_user())
        return super(LoginView, self).form_valid(form)


class LogoutView(generic.RedirectView):
    pattern_name = "home"

    def get(self, request, *args, **kwargs):
        logout(request)
        return super(LogoutView, self).get(request, *args, **kwargs)


class HomePageView(generic.TemplateView):
    template_name = "home.html"

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            try:
                player = self.request.user.player
                self.continue_game = player.game_set.latest().active
            # no games played yet
            except ObjectDoesNotExist:
                self.continue_game = False
        else:
            self.continue_game = False
        return super(HomePageView, self).get(request, *args, **kwargs)

    def get_context_data(self):
        context = super(HomePageView, self).get_context_data()
        context["continue_game"] = self.continue_game
        # the first solution below is optimal as far as the query
        # is concerned but if a player has not won/lost/drawn any game yet
        # then he does not appear in the results, making the lists shorter
        # and messing things up
        #players_won = Player.objects.filter(
        #            game__won_by=Game.PLAYER).annotate(nwon=Count('game'))
        #players_lost = Player.objects.filter(
        #            game__won_by=Game.COMPUTER).annotate(nlost=Count('game'))
        #players_draw = Player.objects.filter(
        #            game__won_by=Game.DRAW).annotate(ndraw=Count('game'))
        #hall_fame = []
        #for t in zip(players_won, players_lost, players_draw):
        #    hall_fame.append((t[0].user.username,
        #                      t[0].nwon, t[1].nlost, t[2].ndraw))

        # so, the best thing to do is to scan each player for his games
        players = Player.objects.all()
        hall_fame = []
        for p in players:
            nwon = p.game_set.filter(won_by=Game.PLAYER).count()
            nlost = p.game_set.filter(won_by=Game.COMPUTER).count()
            ndraw = p.game_set.filter(won_by=Game.DRAW).count()
            player_stats = (p.user.username, nwon, nlost, ndraw)
            hall_fame.append(player_stats)

        hall_fame.sort(key=lambda h: h[1], reverse=True)
        context["hall_fame"] = enumerate(hall_fame, start=1)
        return context

