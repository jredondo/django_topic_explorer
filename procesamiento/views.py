# -*- coding: utf-8 -*-
"""
Sistema de Modelado de Tópicos

Copyleft (@) 2014 CENDITEL nodo Mérida - https://planificacion.cenditel.gob.ve/trac/
"""
## @package django_topic_explorer.procesamiento.views
#
# Vistas y métodos de la aplicación de procesamiento
# @author Rodrigo Boet (rboet at cenditel.gob.ve)
# @author <a href='http://www.cenditel.gob.ve'>Centro Nacional de Desarrollo e Investigación en Tecnologías Libres
# (CENDITEL) nodo Mérida - Venezuela</a>
# @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
# @version 1.3
import os
from shutil import copy
from django.shortcuts import render
from django.views.generic import FormView
from django.core.urlresolvers import reverse_lazy
from django.http import JsonResponse
from django_topic_explorer.settings import PROCESAMIENTO_PATH, BASE_DIR
from utils.freeling import *
from utils.corpusScript import *
from utils.run_lda import generate_comand
from .forms import ProcesamientoForm

class ProcesamientoCreate(FormView):
    """!
    Clase que permite la visualización del formulario de procesamiento
    @author Rodrigo Boet (rboet at cenditel.gob.ve)
    @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
    @date 08-02-2017
    """
    template_name = "procesamiento/index.html"
    form_class = ProcesamientoForm
    success_url = reverse_lazy('procesamiento_index')
    
    def form_valid(self,form):
        """!
        Metodo que permite procesar si el formulario es válido
    
        @author Rodrigo Boet (rboet at cenditel.gob.ve)
        @copyright GNU/GPLv2
        @date 08-02-2017
        @param self <b>{object}</b> Objeto que instancia el método
        @param form <b>{object}</b> Objeto que contiene el formulario
        @return Retorna un redirect a la success_url
        """        
        procesamiento_dir  = form.cleaned_data['procesamiento_dir']
        corpus_dir  = form.cleaned_data['corpus_dir']
        words  = form.cleaned_data['words']
        excluded_words  = form.cleaned_data['excluded_words']
        
        if len(excluded_words)>0:
            excluded_words = excluded_words.split(",")
        
        ## Se crea el directorio del procesamiento
        procesamiento_dir = PROCESAMIENTO_PATH+"/"+procesamiento_dir
        if not os.path.exists(procesamiento_dir):
            os.mkdir(procesamiento_dir)
            
        ## Se preparan los archivos/directorios necesarios para el pre-procesamiento
        self.prepare_files(corpus_dir,procesamiento_dir)
        
        ## Se realiza el freeling y procesamiento con LDA
        self.make_process(procesamiento_dir,words,excluded_words)
        
        if self.request.is_ajax():
            return JsonResponse({"code":True})
        else:
            return super(ProcesamientoCreate, self).form_valid(form)
    
    def prepare_files(self,path,dest):
        """!
        Metodo para copiar los corpus del destino al origen y crear los directorios
    
        @author Rodrigo Boet (rboet at cenditel.gob.ve)
        @copyright GNU/GPLv2
        @date 08-02-2017
        @param self <b>{object}</b> Objeto que instancia el método
        @param path <b>{str}</b> Recibe la ruta de origen
        @param dest <b>{str}</b> Recibe la ruta de destino
        """
        ## Se crea el directorio orig si no existe
        if not os.path.exists(dest+"/orig/"):
            os.mkdir(dest+"/orig/")
        ## Se obtiene una lista de los archivos en el directorio
        list_files = corpus_files = os.listdir(path)
        ## Se copian los archivos del directorio a la raiz de proyecto
        for item in list_files:
            copy(path+"/"+item, dest+"/orig/")
        ## Se crean los directorios necesarios para el pre-procesamiento
        if not os.path.exists(dest+"/lower/"):
            os.mkdir(dest+"/lower/")
        if not os.path.exists(dest+"/pp/"):
            os.mkdir(dest+"/pp/")
        if not os.path.exists(dest+"/lda/"):
            os.mkdir(dest+"/lda/")
        if not os.path.exists(dest+"/freeling/"):
            os.mkdir(dest+"/freeling/")
        if not os.path.exists(dest+"/noaccent/"):
            os.mkdir(dest+"/noaccent/")
            
    def make_process(self, path, word_list, exluded_words):
        """!
        Metodo para realizar el pre-procesamiento y lda
    
        @author Rodrigo Boet (rboet at cenditel.gob.ve)
        @copyright GNU/GPLv2
        @date 09-02-2017
        @param self <b>{object}</b> Objeto que instancia el método
        @param path <b>{str}</b> Recibe la ruta de origen del corpus
        @param word_list <b>{list}</b> Recibe una lista palabras a excluir
        @param exluded_words <b>{list}</b> Recibe una lista de las palabras a excluir
        """
        orig_corpus_path = path + '/orig/'
        lower_corpus_path = path + '/lower/'
        pp_corpus_path = path + '/pp/'
        lda_corpus_path = path + '/lda/'
        
        ## Crea los archivos de puro minusculas
        files_to_lower(orig_corpus_path,lower_corpus_path)
        
        ## Se realiza el pre-procesamiento
        if len(word_list)>1:
            file_words_pp,corpus_words = preprocess(lower_corpus_path,do_fl=True,pos_list=word_list)
        else:
            file_words_pp,corpus_words = preprocess(lower_corpus_path,do_fl=True)
        
        ## Se genera el archivo de vocabulario excluido
        generate_exluded_file(path+"/",pp_corpus_path,file_words_pp,exluded_words)
        
        ## Se generan los archivos .dat
        corpus_script(pp_corpus_path,lda_corpus_path)
        
        ## Se generan los archivos con el LDA
        corpus_dat = lda_corpus_path+'corpus.dat' 
        generate_comand(BASE_DIR,corpus_dat,path,9)
        

