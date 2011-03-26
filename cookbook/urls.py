from django.conf.urls.defaults import *

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^admin/', include(admin.site.urls)),
    (r'^', include('cookbook.recipe.urls')),
    (r'^', include('cookbook.content.urls')),
    (r'^', include('cookbook.user.urls')),
)
