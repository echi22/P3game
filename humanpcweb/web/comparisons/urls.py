from django.conf.urls.defaults import patterns, include, url

from django.contrib import admin
admin.autodiscover()
from web.comparisons import views
urlpatterns = patterns('',

    url(r'^generate$',views.generate),
    
    )