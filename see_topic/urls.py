from django.conf.urls import patterns, include, url
from .views import verTopico
from topic_explorer.views import IrTopic

urlpatterns = patterns('',
    url(r'^$',IrTopic.as_view()),
    url(r'^topicos$', verTopico.as_view() , name='topicos'),
)