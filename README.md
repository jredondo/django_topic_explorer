# django_topic_explorer
This is an alternative (Django based) implementation of this software: https://github.com/inpho/topic-explorer.
By now this is no more than a kind of rudimentary proof of concept we hope to enrich in the forthcoming.

## By now, we use:
- Function based views.
- Global variables: lda_c, lda_c, lda_m.
- An already trained models which must be specified in the corresponding settings variables.
- Urls for requests (Buttons in the interface does not work, see "Using it")

## In the forthcoming, we hope to:
- Provide user interface to select a corpus in the fly (not sure how) from a determined set.
- Not use global variables.
- Develop some per-document visualization.
- ...

## Using it:

...# python manage.py runserver

1) To request a visulization of documents ordered in terms of similarity to a determined topic, then use:
http://127.0.0.1:8000/topic_explorer/topic/70/10/
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^|^^^^^|^^|^^
                  W                 |  X  |Y | Z 
W: App url
X: order by topic
Y: Number of topics
Z: Topic in terms of which documents will be ordered

2) To request a visulization of documents ordered in terms of similarity to a determined document, then use:
http://127.0.0.1:8000/topic_explorer/doc/70/AP881107-0210/
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^|^^^|^^|^^^^^^^^^^^^^^
                  W                 | X |Y |     Z 
W: App url
X: order by document
Y: Number of topics
Z: Document in terms of which the remaining documents will be ordered 

