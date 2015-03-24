from django.conf.urls.defaults import patterns, include, url

from django.contrib import admin
admin.autodiscover()
from web.proteins.users import users
urlpatterns = patterns('',

    #url(r'^create_user$',users.create_user),
    url(r'^login_user$',users.login_user),
    url(r'^logout_user$',users.logout_user),
    url(r'^get_user$',users.get_user),
    url(r'^create_anonymous_user$',users.create_anonymous_user),
    url(r'^register_anonymous$',users.register_anonymous),
    url(r'^login_or_register$',users.login_or_register),
    url(r'^login$',users.login),
    url(r'^register$',users.register),
    #url(r'^highscores$',users.highscores),
    )