from django.conf.urls import include, url
from django.contrib import admin

import settings

urlpatterns = [

    #url(r'^admin/', include(admin.site.urls)),
    url(r'^topic_explorer/', include('topic_explorer.urls')),
    url(r'^procesamiento', include('procesamiento.urls')),
]

"""
if settings.DEBUG:
    urlpatterns += patterns('django.contrib.staticfiles.views',
        url(r'^static/(?P<path>.*)$', 'serve'),
    )
"""
