from django.conf.urls.defaults import *

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^', include('cookbook.content.urls')),
    (r'^', include('cookbook.user.urls')),
    (r'^', include('cookbook.recipe.urls')),

    (r'^admin/', include(admin.site.urls)),
)
