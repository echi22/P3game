from django.conf.urls.defaults import patterns, include, url

from django.contrib import admin
admin.autodiscover()
from web.proteins.game import views
urlpatterns = patterns('',

    url(r'^get_game_instances$','proteins.game.views.get_game_instances_json'),
    url(r'^get_game_scores_for_user$','proteins.game.views.get_game_scores_for_user'),
    url(r'^get_game_settings$','proteins.game.views.get_game_settings'),
    url(r'^choose$','proteins.game.views.choose'),
    url(r'^play$','proteins.game.views.consensus_game'),
    url(r'^show_score','proteins.game.views.show_score'),
    url(r'^get_game_score$','proteins.game.views.get_game_score'),
    url(r'^get_diff$','proteins.game.views.minutes_since_last_time_played'),
    url(r'^get_game_score_for_game$','proteins.game.views.get_game_score_for_game'),
    url(r'^show_highscore_table$','proteins.game.views.show_highscore_table'),
    url(r'^get_game_score_for_game_and_level$','proteins.game.views.get_game_score_for_game_and_level'),
    
    )