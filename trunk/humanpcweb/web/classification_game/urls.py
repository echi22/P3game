from django.conf.urls.defaults import patterns, include, url

from django.contrib import admin
admin.autodiscover()
from web.classification_game import views
urlpatterns = patterns('',

    url(r'^get_game_instance$',views.get_game_instance),
#    url(r'^get_game_data$','proteins.game.views.get_game_data'),
#    url(r'^choose$','proteins.game.views.choose'),
#    url(r'^choose_level$','proteins.game.views.choose_level'),
    url(r'^play$',views.play),
#    url(r'^select_game$','proteins.game.views.select_game'),
#
#    url(r'^save_comparison_percentage$','proteins.game.views.save_comparison_percentage'),
    )