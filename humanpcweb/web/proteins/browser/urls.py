from django.conf.urls.defaults import patterns, include, url


from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',

    url(r'^$','proteins.browser.browser.browse'),
    url(r'^class$','proteins.browser.browser._class'),
    url(r'^fold$','proteins.browser.browser.fold'),
    url(r'^superfamily$','proteins.browser.browser.superfamily'),
    url(r'^family$','proteins.browser.browser.family'),
    url(r'^protein$','proteins.browser.browser.protein'),
    url(r'^generate_images$','proteins.browser.browser.generate_images'),
    )