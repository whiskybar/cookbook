from django.conf.urls.defaults import *

urlpatterns = patterns('cookbook.content.views',
    url(r'^$', 'homepage', name='homepage'),
)
