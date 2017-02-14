# -*- coding: utf-8 -*-
"""
Sistema de Modelado de Tópicos

Copyleft (@) 2014 CENDITEL nodo Mérida - https://planificacion.cenditel.gob.ve/trac/
"""
## @package django_topic_explorer.procesamiento.forms
#
# Formularios de de la aplicación de procesamiento
# @author Rodrigo Boet (rboet at cenditel.gob.ve)
# @author <a href='http://www.cenditel.gob.ve'>Centro Nacional de Desarrollo e Investigación en Tecnologías Libres
# (CENDITEL) nodo Mérida - Venezuela</a>
# @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
# @version 1.3
from django import forms
import os

class ProcesamientoForm(forms.Form):
    """!
    Clase para crear el formulario del procesamiento
    @author Rodrigo Boet (rboet at cenditel.gob.ve)
    @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
    @date 08-02-2017
    """
    ## Campo con el nombre del directorio a procesar
    procesamiento_dir = forms.CharField(label=('Nombre del directorio'))
    
    ## Campo con la ruta donde estan los corpus originales
    corpus_dir = forms.CharField(label=('Directorio de Corpus'))
    
    ## Palabras a excluir
    words = forms.MultipleChoiceField(label = ('Palabras'),choices = [('V', 'verbos'),('A', 'adjetivos'), ('N', 'sustantivos'),
        ('R', 'adverbios'),('D', 'determinantes'),('P', 'pronombres'),('C', 'conjunciones'),('I', 'interjecciones'),('S', 'preposiciones')],
        required=False)
    
    ## Listado de palabras excluidas por el usuario
    excluded_words = forms.CharField(label=('Palabras Excluidas'),widget=forms.Textarea,required = False)
    
    def clean_corpus_dir(self):
        corpus_dir = self.cleaned_data['corpus_dir']
        if not os.path.exists(corpus_dir):
            raise forms.ValidationError("La Ruta Solicitada no existe")
        return corpus_dir
    
    
