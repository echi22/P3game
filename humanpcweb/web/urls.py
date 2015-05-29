from django.conf.urls.defaults import patterns, include, url

from django.contrib import admin
from web.proteins.browser import urls as browser_URLs

admin.autodiscover()

urlpatterns = patterns('',
    #url(r'^$', 'web.views.home', name='home'),
    # url(r'^web/', include('web.foo.urls')),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^browser/',include(browser_URLs)),
    url(r'^researcher/',include('web.researcher.urls')),
    url(r'^users/',include('web.proteins.users.urls')),
    url(r'^game/',include('web.proteins.game.urls')),
#    url(r'^classification_game/',include('web.classification_game.urls')),
#    url(r'^/comparisons/',include('web.comparisons.urls')),
    url(r'^proteins/',include('web.proteins.urls')),
    url(r'^login', 'web.views.views.login'),



    url(r'^redirect$','views.views.redirect'),
    url(r'^$','web.views.views.index'),
    )