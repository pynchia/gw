from django.conf.urls import patterns, include, url
from django.contrib import admin
from guesswu.views import HomePageView, SignUpView

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'guesswu.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^$', HomePageView.as_view(), name='home'),
    url(r'^accounts/signup/$', SignUpView.as_view(), name='signup'),
    url(r'^accounts/login/$', 'django.contrib.auth.views.login', name='login'),
#    url(r'^play/', include('play.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
