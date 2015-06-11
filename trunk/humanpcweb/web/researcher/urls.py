from django.conf.urls.defaults import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^download_comparisons$','researcher.views.download_comparisons'),
    url(r'^upload_classification$','researcher.views.upload_classification'),
    url(r'^load_proteins_from_server$','researcher.views.load_proteins_from_server'),
    url(r'^upload_proteins$','researcher.views.upload_proteins'),
    url(r'^regenerate_protein_images$','researcher.views.regenerate_protein_images'),
    url(r'^clear_game_instances$','researcher.views.clear_game_instances'),
    url(r'^clear_scores$','researcher.views.clear_scores'),
    url(r'^clear_proteins$','researcher.views.clear_proteins'),
    url(r'^clear_classification$','researcher.views.clear_classification'),
    url(r'^update_corrects$','researcher.views.update_corrects'),
    url(r'^simulate_cath$','researcher.views.simulate_cath'),
    url(r'^$','researcher.views.index'),
    )