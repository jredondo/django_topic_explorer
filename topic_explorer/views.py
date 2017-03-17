# -*- coding: utf-8 -*-
"""
Sistema de Modelado de Tópicos

Copyleft (@) 2014 CENDITEL nodo Mérida - https://planificacion.cenditel.gob.ve/trac/
"""
## @package django_topic_explorer.topic_explorer
#
# Métodos de la Vista, para visualizar los tópicos
# @author Jorge Redondo (jredondo at cenditel.gob.ve)
# @author <a href='http://www.cenditel.gob.ve'>Centro Nacional de Desarrollo e Investigación en Tecnologías Libres
# (CENDITEL) nodo Mérida - Venezuela</a>
# @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
# @version 1.3

from django.shortcuts import render

from django.conf import settings

from django.http import HttpResponse, HttpResponseServerError

import json

from utils.ldac2vsm import *
from utils.json_data import *
#from vsm.corpus import Corpus
#from vsm.model.ldacgsmulti import LdaCgsMulti as LCM
from vsm.viewer.ldagibbsviewer import LDAGibbsViewer as LDAViewer
from vsm.viewer.wrappers import doc_label_name

from django.views.generic import TemplateView
from django.http import JsonResponse
from django.core.urlresolvers import reverse

from StringIO import StringIO
import csv

from django_topic_explorer.settings import FILES_PATH
from django_topic_explorer.settings import LDA_DATA_PATH 
from django_topic_explorer.settings import LDA_CORPUS_FILE 
from django_topic_explorer.settings import LDA_VOCAB_FILE 
from django_topic_explorer.settings import LDA_CORPUS_DIR 


#path = settings.PATH 
#corpus_file = settings.CORPUS_FILE
#context_type = settings.CONTEXT_TYPE
context_type = 'propesta'
#model_pattern = settings.MODEL_PATTERN
topics = settings.TOPICS
#corpus_name = settings.CORPUS_NAME

corpus_link = settings.CORPUS_LINK
topics_range = [int(item) for item in settings.TOPICS.split(',')]
doc_title_format = settings.DOC_TITTLE_FORMAT
doc_url_format = settings.DOC_URL_FORMAT

global k_param
k_param = None
global lda_c,lda_m, lda_v

# Integración LDA-c topic_explorer
lda_c,lda_m = corpus_model(50,LDA_DATA_PATH.format(50),
                           LDA_CORPUS_FILE,
                           LDA_VOCAB_FILE,
                           LDA_CORPUS_DIR)
#lda_c = Corpus.load(corpus_file)
#lda_c.save('/home/jredondo/tmp/corpus.npz')
lda_v = LDAViewer(lda_c, lda_m)

#lda_m = LCM.load(model_pattern.format(k))
label = lambda x: x

def dump_exception():
    """!
    Función para captar los errores e imprimirlos

    @author Jorge Redondo (jredondo at cenditel.gob.ve)
    @copyright GNU/GPLv2
    @param request <b>{object}</b> Objeto que mantiene la peticion
    @return Retorna una respuesta http con el error
    """ 
    import sys,traceback
    exc_type, exc_value, exc_traceback = sys.exc_info()
    print "*** print_tb:"
    traceback.print_tb(exc_traceback, limit=1, file=sys.stdout)
    print "*** print_exception:"
    traceback.print_exception(exc_type, exc_value, exc_traceback, limit=2, file=sys.stdout)
    return HttpResponseServerError(str(exc_value))


def doc_topic_csv(request, doc_id):
    """!
    Función para retornar un documento en csv

    @author Jorge Redondo (jredondo at cenditel.gob.ve)
    @copyright GNU/GPLv2
    @param request <b>{object}</b> Objeto que mantiene la peticion
    @param doc_id <b>{string}</b> Recibe el número del documento
    @return Retorna los datos del documento
    """
    global lda_v
    try:
        data = lda_v.doc_topics(doc_id)

        output=StringIO()
        writer = csv.writer(output)
        writer.writerow(['topic','prob'])
        writer.writerows([(t, "%6f" % p) for t,p in data])

        return HttpResponse(output.getvalue())
    except:
        return dump_exception()

def doc_csv(request, k,doc_id,threshold=0.2):
    """!
    Función para retornar la data de los tópicos en csv

    @author Jorge Redondo (jredondo at cenditel.gob.ve)
    @copyright GNU/GPLv2
    @param request <b>{object}</b> Objeto que mantiene la peticion
    @param k <b>{int}</b> Recibe el número de tópicos a mostrar
    @param doc_id <b>{string}</b> Recibe el número de tópicos
    @param threshold <b>{int}</b> Recibe el limite estadístico
    @return Retorna el render de la vista
    """
    global k_param, lda_c, lda_m, lda_v
    try:
        if k != k_param:
            k_param = k
            generate_topic(k_param)
        data = lda_v.sim_doc_doc(doc_id)

        output=StringIO()
        writer = csv.writer(output)
        writer.writerow(['doc','prob'])
        writer.writerows([(d, "%6f" % p) for d,p in data if p > threshold])

        return HttpResponse(output.getvalue())
    except:
        return dump_exception()

def topic_json(request,k,topic_no, N=40):
    """!
    Función para retornar la data de los tópicos en json

    @author Jorge Redondo (jredondo at cenditel.gob.ve)
    @copyright GNU/GPLv2
    @param request <b>{object}</b> Objeto que mantiene la peticion
    @param k <b>{int}</b> Recibe el número de tópicos a mostrar
    @param topic_no <b>{string}</b> Recibe el número de tópicos
    @param N <b>{int}</b> Recibe la cantidad
    @return Retorna el render de la vista
    """
    global k_param, lda_c, lda_m, lda_v
    try:
        if k != k_param:
            k_param = k
            generate_topic(k_param,lda_c,lda_m,lda_v)
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
    except:
        return dump_exception()

def doc_topics(request,doc_id, N=40):
    """!
    Función para retornar la data de los documentos en json

    @author Jorge Redondo (jredondo at cenditel.gob.ve)
    @copyright GNU/GPLv2
    @param request <b>{object}</b> Objeto que mantiene la peticion
    @param doc_id <b>{string}</b> Recibe el número del documento
    @param N <b>{int}</b> Recibe la cantidad
    @return Retorna el render de la vista
    """
    global lda_v
    try:
        if lda_v == None:
            generate_topic(k_param)
        try:
            N = int(request.query.n)
        except:
            pass
        js = doc_json(lda_v,doc_id,N)
        return HttpResponse(json.dumps(js))
    except:
        return dump_exception()
    
    
def topics(request):
    """!
    Función para servir los tópicos como un json

    @author Jorge Redondo (jredondo at cenditel.gob.ve)
    @copyright GNU/GPLv2
    @param request <b>{object}</b> Objeto que mantiene la peticion
    @return Retorna el objeto json
    """ 
    global lda_v
    try:
        js=populateJson(lda_v)
        return HttpResponse(json.dumps(js))
    except:
        return dump_exception()
    

def docs(request):
    """!
    Función para servir los documentos como un json

    @author Jorge Redondo (jredondo at cenditel.gob.ve)
    @copyright GNU/GPLv2
    @param request <b>{object}</b> Objeto que mantiene la peticion
    @return Retorna el objeto json
    """
    global lda_v
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
    """!
    Función para visualizar el index del proyecto

    @author Jorge Redondo (jredondo at cenditel.gob.ve)
    @copyright GNU/GPLv2
    @param request <b>{object}</b> Objeto que mantiene la peticion
    @return Retorna el render de la vista
    """
    try:
        template_name = 'topic_explorer/index.html'
        return render(request,template_name,
            {'filename':None,
             'corpus_link' : corpus_link,
             'context_type' : context_type,
             'topics_range' : topics_range,
             'doc_title_format' : doc_title_format,
             'doc_url_format' : doc_url_format})
    except:
        return dump_exception()

def visualize(request,k,filename=None,topic_no=None):
    """!
    Función para visualizar los tópicos

    @author Jorge Redondo (jredondo at cenditel.gob.ve)
    @copyright GNU/GPLv2
    @param request <b>{object}</b> Objeto que mantiene la peticion
    @param k <b>{int}</b> Recibe el número de tópicos a mostrar
    @param filename <b>{string}</b> Recibe el nombre del  archivo
    @param topic_no <b>{int}</b> Recibe el número de tópico
    @return Retorna el render de la vista
    """
    global k_param,lda_c,lda_m,lda_v
    try:
        if k != k_param:
            k_param = k
            generate_topic(k_param)
        template_name = 'topic_explorer/index.html'
        return render(request,template_name,
            {'filename':filename,
             'k_param':k_param,
             'topic_no':topic_no,
             'corpus_link' : corpus_link,
             'context_type' : context_type,
             'topics_range' : topics_range,
             'doc_title_format' : doc_title_format,
             'doc_url_format' : doc_url_format})
    except:
        return dump_exception()
    
def generate_topic(k_param):
    """!
    Función para generar los tópicos

    @author Rodrigo Boet (rboet at cenditel.gob.ve)
    @copyright GNU/GPLv2
    @date 13-03-2017
    @param k_param <b>{object}</b> Objeto que contiene la cantidad de tópicos
    @param lda_c <b>{object}</b> Objeto que perteneciente al lda
    @param lda_m <b>{object}</b> Objeto que perteneciente al lda
    @param lda_v <b>{object}</b> Objeto que perteneciente al lda
    """
    global lda_c,lda_m,lda_v
    lda_c,lda_m = corpus_model(k_param,LDA_DATA_PATH.format(k_param),
                       LDA_CORPUS_FILE,
                       LDA_VOCAB_FILE,
                       LDA_CORPUS_DIR)
    lda_v = LDAViewer(lda_c, lda_m)

class IrTopic(TemplateView):
    """!
    Clase que permite la visualización de un archivo en particular
    @author Rodrigo Boet (rboet at cenditel.gob.ve)
    @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
    @date 31-07-2015
    """
    
    template_name='topic_explorer/verTopico.html'
    
    
    def get(self, request, propuesta = None):
        """!
        Metodo que permite procesar las peticiones por get, con el fin de mostrar el documento
    
        @author Rodrigo Boet (rboet at cenditel.gob.ve)
        @copyright GNU/GPLv2
        @date 31-07-2015
        @param self <b>{object}</b> Objeto que instancia el método
        @param request <b>{object}</b> Objeto que mantiene la peticion
        @param propuesta <b>{int}</b> Recibe el número de la propuesta
        @return Retorna el render de la vista
        """
        global lda_v
        #Obtnener json
        Topic_Json = populateJson(lda_v)
        Topic_Json = json.dumps(Topic_Json)
        topicos = json.loads(Topic_Json)
        N = len(topicos)
        Docs = doc_json(lda_v,propuesta,N)
        Docs = json.dumps(Docs)
        documentos = self.obtenerDocumento(json.loads(Docs),propuesta)
        documentos = json.dumps(documentos)
        mi_color = []
        mi_color = self.obtenerValores(topicos)
        mi_color = json.dumps(mi_color)
        topicos = json.dumps(topicos)
        #carga el pre-procesado del archivo en una variable
        texto=''
        direccion = FILES_PATH + '/'+ propuesta
        try:
            archivo = open(direccion,'r')
            texto=archivo.read()
            archivo.close()
        except:
            return dump_exception()
            texto='No se encontro el documento'
        return render(request,self.template_name,
                      {'topicos':topicos,
                       'propuesta':propuesta,
                       'color':mi_color,
                       'texto':texto,
                       'documento':documentos})
    
    def obtenerValores(self,topicos):
        """!
        Metodo para obtener los colores del json
    
        @author Rodrigo Boet (rboet at cenditel.gob.ve)
        @copyright GNU/GPLv2
        @date 31-07-2015
        @param self <b>{object}</b> Objeto que instancia el método
        @param topicos <b>{dict}</b> Recibe un diccionario con los topicos 
        @return Retorna un diccionario con los colores
        """
        my_topic=[]
        for x in topicos:
            my_topic.append(topicos[x]['color'])
        return my_topic
    
    def obtenerDocumento(self,docs,propuesta):
        """!
        Metodo para obtener un documento
    
        @author Rodrigo Boet (rboet at cenditel.gob.ve)
        @copyright GNU/GPLv2
        @date 03-02-2016
        @param self <b>{object}</b> Objeto que instancia el método
        @param docs <b>{dict}</b> Recibe un diccionario con los documentos
        @param propuesta <b>{int}</b> Recibe el número de la propuesta
        @return Retorna un diccionario con los colores
        """
        for x in docs:
            if(x['doc']==propuesta):
                return x

class ListTopics(TemplateView):
    """!
    Clase que permite la visualización de un archivo en particular
    @author Rodrigo Boet (rboet at cenditel.gob.ve)
    @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
    @date 13-03-2017
    """
    
    template_name='topic_explorer/listTopics.html'
    
    def get_context_data(self,**kwargs):
        """!
        Metodo que permite cargar de nuevo valores en los datos de contexto de la vista
    
        @author Rodrigo Boet (rboet at cenditel.gob.ve)
        @copyright GNU/GPLv2
        @date 13-03-2017
        @param self <b>{object}</b> Objeto que instancia la clase
        @param kwargs <b>{object}</b> Objeto que contiene los datos de contexto
        @return Retorna los datos de contexto
        """
        kwargs['topics_range'] = topics_range
        return super(ListTopics, self).get_context_data(**kwargs)
    
    
def generate_topics(request):
    """!
    Metodo que genera una lista de los tópicos dado un párametro k

    @author Rodrigo Boet (rboet at cenditel.gob.ve)
    @copyright GNU/GPLv2
    @date 13-03-2017
    @param request <b>{object}</b> Recibe la peticion
    @return Retorna el json con las subunidades que consiguió
    """
    global lda_v
    # Recibe por get el id del insumo
    k_param = request.GET.get('k', None)
    
    if(k_param):
        if(int(k_param) in topics_range):
            generate_topic(k_param)
            js = populateJson(lda_v)
            return JsonResponse(js,safe=False)
        return JsonResponse("El párametro k es inválido",safe=False)
    return JsonResponse("Debe enviar el párametro k",safe=False)

    
        