from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponseRedirect
from django.views import generic
# from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

from . import models

class NewGameView(generic.RedirectView):
    pattern_name = "play"

    def get(self, request, *args, **kwargs):

        # close any pending game

        # create a new game

        return super(NewGameView, self).get(request, *args, **kwargs)

class PlayGameView(generic.TemplateView):
    template_name = "play/play.html"

