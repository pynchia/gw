from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required
from . import views

urlpatterns = patterns('',
    url(r'^new/$',
        login_required(views.NewGameView.as_view()),
        name='newgame'),
    url(r'^play/$',
        login_required(views.PlayGameView.as_view()),
        name='playgame'),
    url(r'^feat/(?P<feat_id>\d+)/$',
        login_required(views.PickFeatureView.as_view()),
        name='pickfeat'),
)
