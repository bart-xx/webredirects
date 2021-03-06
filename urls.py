from django.conf.urls.defaults import *

urlpatterns = patterns('',
    (r'^cache/status/$', 'webredirects.memcached_status.views.summary'),
    (r'^accounts/login/$', 'django.contrib.auth.views.login', {'template_name': 'login.html'}),
    (r'^accounts/logout/$', 'django.contrib.auth.views.logout'),
    (r'^', include('django.contrib.admin.urls')),
)
