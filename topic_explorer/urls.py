from django.conf.urls import include, url

from topic_explorer.views import *


from django.contrib import admin
admin.autodiscover()

urlpatterns = [
    url(r'^doc_topics/(?P<doc_id>\d+)/$', doc_topic_csv, name='doc_topic_csv'),
    url(r'^docs/(?P<k>\d+)/(?P<doc_id>.+)/$',doc_csv , name='doc_csv'),
    url(r'^topics/(?P<k>\d+)/(?P<topic_no>\d+)/$', topic_json , name='topic_json'),
    url(r'^docs_topics/(?P<doc_id>.+)/$', doc_topics , name='doc_topics'),
    url(r'^topics.json/$', topics , name='topics'),
    url(r'^docs.json/$', docs , name='docs'),
    url(r'^$', index , name='index'),
    url(r'^doc/(?P<k>\d+)/(?P<filename>.+)/$', visualize , name='visualize_doc'),
    url(r'^topic/(?P<k>\d+)/(?P<topic_no>\d+)/$', visualize , name='visualize'),
    url(r'^see_topic/(?P<propuesta>.+)/$',IrTopic.as_view(),name='see_topic'),
    url(r'^topic_list$', ListTopics.as_view() , name='list_topic'),
]

## Url por ajax

urlpatterns += [
    url(r'^generate_topics$', generate_topics , name='generate_topics'),
]