from django.conf.urls import patterns, include, url

from topic_explorer.views import *


from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^doc_topics/(?P<doc_id>\d+)/$', doc_topic_csv, name='doc_topic_csv'),
    url(r'^docs/(?P<doc_id>)\d+/$',doc_csv , name='doc_csv'),
    url(r'^topics/(?P<k_param>\d+)/(?P<topic_no>\d+)/$', topic_json , name='topic_json'),
    url(r'^docs_topics/(?P<doc_id>.+)/$', doc_topics , name='doc_topics'),
    url(r'^topics.json/$', topics , name='topics'),
    url(r'^docs.json/$', docs , name='docs'),
    url(r'^icons/$', icons , name='icons'),
    url(r'^$', index , name='index'),
    url(r'^doc/(?P<k_param>\d+)/(?P<filename>.+)/$', visualize , name='visualize'),
    url(r'^topic/(?P<k_param>\d+)/(?P<topic_no>\d+)/$', visualize , name='visualize'),

)

"""
urlpatterns = patterns('',
    url(r'^doc_topics/(<doc_id>)/$', doc_topic_csv, name='doc_topic_csv'),
    url(r'^docs/(<doc_id>)/$',doc_csv , name='doc_csv'),
    url(r'^topics/(<topic_no>)/$', topic_json , name='topic_json'),
    url(r'^docs_topics/(<doc_id>)/$', doc_topics , name='doc_topics'),
    url(r'^topics/$', topics , name='topics'),
    url(r'^docs.json/$', docs , name='docs'),
    url(r'^icons/$', icons , name='icons'),
    url(r'^$', index , name='index'),
    url(r'^doc/(<filename>)/$', send_static , name='send_static'),
)
"""
