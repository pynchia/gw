from django.conf.urls import patterns, include, url
from django.contrib import admin
from guesswu import views

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'guesswu.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
#    url(r'^play/', include('play.urls')),
    (r'^$', views.HomePageView.as_view(), name='home'),
    (r'^accounts/login/$', 'django.contrib.auth.views.login'),
    url(r'^admin/', include(admin.site.urls)),
)
