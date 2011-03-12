from django.conf.urls.defaults import *

urlpatterns = patterns('cookbook.recipe.views',
    url(r'^(?P<username>[^/]+)/(?P<recipe_slug>[^/]+)/$', 'recipe_detail', name='recipe_detail'),
    url(r'^add/$', 'recipe_add', name='recipe_add'),
)
