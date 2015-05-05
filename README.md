# django_topic_explorer
This is an alternative (Django based) implementation of this software: https://github.com/inpho/topic-explorer.
By now this is no more than a kind of rudimentary proof of concept we hope to enrich in the forthcoming.

## By now, we use:
- Function based views.
- Global variables: lda_c, lda_c, lda_m.
- An already trained models which must be specified in the corresponding settings variables.
- Urls for requests (Buttons in the interface does not work, see "Using it")

## In the forthcoming, we hope to:
- Provide user interface to select a corpus on the fly (not sure how) from a determined set.
- Not use global variables.
- Develop some per-document visualization.
- ...

## Using it:

...# python manage.py runserver

1) To request a visulization of documents ordered in terms of similarity to a determined topic, then use:
http://127.0.0.1:8000/topic_explorer/topic/70/10/ <br />

http://127.0.0.1:8000/topic_explorer --> App Url <br />
/topic --> Order by topic <br />
/70    --> Model with 70 topics <br />
/10    --> Topic (from the topic legend) in terms of which documents will be ordered <br />


2) To request a visulization of documents ordered in terms of similarity to a determined document, then use:
http://127.0.0.1:8000/topic_explorer/doc/70/AP881107-0210/ <br />

http://127.0.0.1:8000/topic_explorer/ --> App url <br />
/doc   --> Order by document <br />
/70    --> Number of topics <br />
/AP881107-0210  --> Document in terms of which the remaining documents will be ordered  <br />

