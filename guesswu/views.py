from django.core.urlresolvers import reverse_lazy
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect
from django.views import generic
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

from play.models import Player

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
            except ObjectDoesNotExist:
                self.continue_game = False
        return super(HomePageView, self).get(request, *args, **kwargs)

    def get_context_data(self):
        context = super(HomePageView, self).get_context_data()
        context["continue_game"] = getattr(self, "continue_game", False)
        return context

