from django.conf.urls.defaults import *

urlpatterns = patterns('cookbook.user.views',
    url(r'^(?P<username>[^/]+)/$', 'user_homepage', name='user_homepage'),
)
