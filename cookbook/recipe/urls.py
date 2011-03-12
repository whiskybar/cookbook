from django.conf.urls.defaults import *

urlpatterns = patterns('cookbook.user.views',
    url(r'^(?:<username>\S+)/(?:<recipe_slug>\S+)/$', 'recipe_detail', name='recipe_detail'),
)
