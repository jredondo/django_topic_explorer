from django.conf.urls import patterns, include, url
from django.contrib import admin

import settings

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'django_lda_fw.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    #url(r'^admin/', include(admin.site.urls)),
    url(r'^topic_explorer/', include('topic_explorer.urls')),
)
"""
if settings.DEBUG:
    urlpatterns += patterns('django.contrib.staticfiles.views',
        url(r'^static/(?P<path>.*)$', 'serve'),
    )
"""
