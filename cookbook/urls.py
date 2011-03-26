from django.conf import settings
from django.conf.urls.defaults import *
from django.conf.urls.static import static

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^admin/', include(admin.site.urls)),
    (r'^photologue/', include('photologue.urls')),
    (r'^', include('cookbook.recipe.urls')),
    (r'^', include('cookbook.content.urls')),
    (r'^', include('cookbook.user.urls')),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
