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
    (r'^i18n/', include('django.conf.urls.i18n')),

    url(r'^admin/', include(admin.site.urls)),
    (r'^login/$', 'mychat.views.login_user'),
    (r'^post/$', 'mychat.views.post'),
    (r'^get/$', 'mychat.views.get'),
    (r'^vchat_req/$', 'mychat.views.vchat_req'),
    (r'^vchat_join/$', 'mychat.views.vchat_join'),

)
