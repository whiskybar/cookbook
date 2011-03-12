from django.conf.urls.defaults import *

urlpatterns = patterns('cookbook.user.views',
    url(r'^(?:<username>\S+)/$', 'user_homepage', name='user_homepage'),
)
