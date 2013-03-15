from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'schat.views.home', name='home'),
    # url(r'^schat/', include('schat.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    (r'^login/$', 'mychat.views.login_user'),
    (r'^post/$', 'mychat.views.post'),
    (r'^get/$', 'mychat.views.get'),

)
