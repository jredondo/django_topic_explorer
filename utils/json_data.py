# -*- coding: utf-8 -*-
"""
Sistema de Modelado de Tópicos

Copyleft (@) 2014 CENDITEL nodo Mérida - https://planificacion.cenditel.gob.ve/trac/
"""
## @package django_topic_explorer.utils
#
# Métodos para el trato de json
# @author Jorge Redondo (jredondo at cenditel.gob.ve)
# @author <a href='http://www.cenditel.gob.ve'>Centro Nacional de Desarrollo e Investigación en Tecnologías Libres
# (CENDITEL) nodo Mérida - Venezuela</a>
# @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
# @version 1.3
from utils import colorlib
import itertools

label = lambda x: x

def populateJson(lda_v):
    """!
    Función para cargar un json

    @author Jorge Redondo (jredondo at cenditel.gob.ve)
    @copyright GNU/GPLv2
    @param lda_v <b>{object}</b> Recibe el objeto del lda
    @return Retorna un json
    """
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
        js[str(i)].update({'words' : dict([(w, p) for w,p in topic[:20]])})
    return js


def doc_json(lda_v,doc_id,N=40):
    """!
    Función para cargar los documentos y sus tópicos en un json

    @author Jorge Redondo (jredondo at cenditel.gob.ve)
    @copyright GNU/GPLv2
    @param lda_v <b>{object}</b> Recibe el objeto del lda
    @param doc_id <b>{string}</b> Recibe el id del documento
    @param N <b>{object}</b> Recibe la cantidad
    @return Retorna un json
    """
    if doc_id!='null':
        try:
            if N > 0:
                data = lda_v.dist_doc_doc(doc_id)[:N]
            else:
                data = lda_v.dist_doc_doc(doc_id)[N:]
                data = reversed(data)
            #data = docs_data(lda_v,doc_id,N)
            docs = [doc for doc,prob in data]
            doc_topics_mat = lda_v.doc_topics(docs)
    
            js = []
            for doc_prob, topics in zip(data, doc_topics_mat):
                doc, prob = doc_prob
                js.append({'doc' : doc, 'label': label(doc), 'prob' : 1-prob,
                    'topics' : dict([(str(t), p) for t,p in topics])})
            return js
        except:
            import sys,traceback
            exc_type, exc_value, exc_traceback = sys.exc_info()
            print "*** print_tb:"
            traceback.print_tb(exc_traceback, limit=1, file=sys.stdout)
            print "*** print_exception:"
            traceback.print_exception(exc_type, exc_value, exc_traceback, limit=2, file=sys.stdout)
            return "error"
    



