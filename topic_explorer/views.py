from django.shortcuts import render

from django.conf import settings

from django.http import HttpResponse, HttpResponseRedirect, HttpResponseServerError, StreamingHttpResponse

import json

from utils import colorlib
import itertools
from vsm.corpus import Corpus
from vsm.model.ldacgsmulti import LdaCgsMulti as LCM
from vsm.viewer.ldagibbsviewer import LDAGibbsViewer as LDAViewer
from vsm.viewer.wrappers import doc_label_name
from django.core import serializers

from django.views.generic import TemplateView
from django.core.urlresolvers import reverse

from StringIO import StringIO
import csv

from django_topic_explorer.settings import URL_COMUN
from django.utils.safestring import mark_safe
from django_topic_explorer.settings import FILES_PATH

#path = settings.PATH 
corpus_file = settings.CORPUS_FILE
context_type = settings.CONTEXT_TYPE
model_pattern = settings.MODEL_PATTERN
topics = settings.TOPICS
corpus_name = settings.CORPUS_NAME
icons = settings.ICONS

corpus_link = settings.CORPUS_LINK
topics_range = [int(item) for item in settings.TOPICS.split(',')]
doc_title_format = settings.DOC_TITTLE_FORMAT
doc_url_format = settings.DOC_URL_FORMAT

#global lda_m, lda_v

lda_c = Corpus.load(corpus_file)
#lda_m = LCM.load(model_pattern.format(k))
#lda_v = LDAViewer(lda_c, lda_m)
label = lambda x: x

def dump_exception():
    import sys,traceback
    exc_type, exc_value, exc_traceback = sys.exc_info()
    print "*** print_tb:"
    traceback.print_tb(exc_traceback, limit=1, file=sys.stdout)
    print "*** print_exception:"
    traceback.print_exception(exc_type, exc_value, exc_traceback, limit=2, file=sys.stdout)
    return HttpResponseServerError(str(exc_value))


def doc_topic_csv(request, doc_id):
    data = lda_v.doc_topics(doc_id)

    output=StringIO()
    writer = csv.writer(output)
    writer.writerow(['topic','prob'])
    writer.writerows([(t, "%6f" % p) for t,p in data])

    return HttpResponse(output.getvalue())

def doc_csv(request, k_param,doc_id,threshold=0.2):
    lda_m = LCM.load(model_pattern.format(k_param))
    lda_v = LDAViewer(lda_c, lda_m)
    data = lda_v.sim_doc_doc(doc_id)

    output=StringIO()
    writer = csv.writer(output)
    writer.writerow(['doc','prob'])
    writer.writerows([(d, "%6f" % p) for d,p in data if p > threshold])

    return HttpResponse(output.getvalue())

def topic_json(request,k_param,topic_no, N=40):
    #global lda_v
    lda_m = LCM.load(model_pattern.format(k_param))
    lda_v = LDAViewer(lda_c, lda_m)
    try:
        N = int(request.query.n)
    except:
        pass

    if N > 0:
        data = lda_v.dist_top_doc([int(topic_no)])[:N]
    else:
        data = lda_v.dist_top_doc([int(topic_no)])[N:]
        data = reversed(data)

    docs = [doc for doc,prob in data]
    doc_topics_mat = lda_v.doc_topics(docs)

    js = []
    for doc_prob, topics in zip(data, doc_topics_mat):
        doc, prob = doc_prob
        js.append({'doc' : doc, 'label': label(doc), 'prob' : 1-prob,
            'topics' : dict([(str(t), p) for t,p in topics])})
    return HttpResponse(json.dumps(js))

def doc_topics(request,doc_id, N=40):
    try:
        try:
            N = int(request.query.n)
        except:
            pass
        if N > 0:
            data = lda_v.dist_doc_doc(doc_id)[:N]
        else:
            data = lda_v.dist_doc_doc(doc_id)[N:]
            data = reversed(data)

        docs = [doc for doc,prob in data]
        doc_topics_mat = lda_v.doc_topics(docs)

        js = []
        for doc_prob, topics in zip(data, doc_topics_mat):
            doc, prob = doc_prob
            js.append({'doc' : doc, 'label': label(doc), 'prob' : 1-prob,
                'topics' : dict([(str(t), p) for t,p in topics])})
        return HttpResponse(json.dumps(js))
    except:
        return dump_exception()

def topics(request):
    try:
        js=populateJson()
        return HttpResponse(json.dumps(js))
    except:
        return dump_exception()
    
def populateJson():
    # populate entropy values
    data = lda_v.topic_oscillations()

    colors = [itertools.cycle(cs) for cs in zip(*colorlib.brew(3,n_cls=4))]
    factor = len(data) / len(colors)

    js = {}
    for rank,topic_H in enumerate(data):
        topic, H = topic_H
        js[str(topic)] = {
            "H" : H,
            "color" : colors[min(rank / factor, len(colors)-1)].next()
        }

    # populate word values
    data = lda_v.topics()
    for i,topic in enumerate(data):
        js[str(i)].update({'words' : dict([(w.decode('unicode-escape'), p) for w,p in topic[:20]])})
    return js


def docs(request):
    try:
        docs = lda_v.corpus.view_metadata(context_type)[doc_label_name(context_type)]
        js = list()
        for doc in docs:
            js.append({
                'id': doc,
                'label' : label(doc)
            })

        return HttpResponse(json.dumps(js))
    except:
        return dump_exception()

def index(request):
    global lda_m,lda_v
    lda_m = LCM.load(model_pattern.format(10))
    lda_v = LDAViewer(lda_c, lda_m)
    template_name = 'topic_explorer/index.html'
    return render(request,template_name,
        {'filename':None,
         'corpus_name' : corpus_name,
         'corpus_link' : corpus_link,
         'context_type' : context_type,
         'topics_range' : topics_range,
         'doc_title_format' : doc_title_format,
         'doc_url_format' : doc_url_format})

def visualize(request,k_param,filename=None,topic_no=None):
    global lda_m,lda_v
    lda_m = LCM.load(model_pattern.format(k_param))
    lda_v = LDAViewer(lda_c, lda_m)
    template_name = 'topic_explorer/index.html'
    return render(request,template_name,
        {'filename':filename,
         'k_param':k_param,
         'topic_no':topic_no,
         'corpus_name' : corpus_name,
         'corpus_link' : corpus_link,
         'context_type' : context_type,
         'topics_range' : topics_range,
         'doc_title_format' : doc_title_format,
         'doc_url_format' : doc_url_format})

class IrTopic(TemplateView):
    template_name='topic_explorer/verTopico.html'
    def post(self, request, *args, **kwargs):
        propuesta = request.POST['nombre_propuesta']
        #url = reverse('verTopicos')
        #Obtnener json
        Topic_Json = populateJson()
        Topic_Json = json.dumps(Topic_Json)
        topicos = json.loads(Topic_Json)
        mi_color = []
        mi_color = self.obtenerValores(topicos)
        mi_color = json.dumps(mi_color)
        topicos = json.dumps(topicos)
        #print topicos
        #carga el pre-procesado del archivo en una variable
        texto=''
        direccion = FILES_PATH + '/'+ propuesta
        try:
            archivo = open(direccion,'r')
            texto=archivo.read()
            archivo.close()
        except:
            text='No se encontro el documento'
        return render(request,self.template_name,
                      {'topicos':topicos,
                       'propuesta':propuesta,
                       'color':mi_color,
                       'texto':texto})
    
    def obtenerValores(self,topicos):#funcion para obtener los colores del json
        my_topic=[]
        for x in topicos:
            my_topic.append(topicos[x]['color'])
        return my_topic
