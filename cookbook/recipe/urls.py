from django.conf.urls.defaults import *

urlpatterns = patterns('cookbook.recipe.views',
    url(r'^(?P<author>[^/]+)/add/$', 'recipe_edit', name='recipe_add'),
    url(r'^(?P<author>[^/]+)/(?P<slug>[^/]+)/$', 'recipe_detail', name='recipe_detail'),
    url(r'^(?P<author>[^/]+)/(?P<slug>[^/]+)/edit/$', 'recipe_edit', name='recipe_edit'),
    url(r'^(?P<author>[^/]+)/(?P<slug>[^/]+)/delete/$', 'recipe_delete', name='recipe_delete'),
    url(r'^(?P<author>[^/]+)/(?P<slug>[^/]+)/upload/$', 'gallery_upload', name='gallery_upload'),
)
