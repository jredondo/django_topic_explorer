# -*- coding: utf-8 -*-
"""
Sistema de Modelado de Tópicos

Copyleft (@) 2014 CENDITEL nodo Mérida - https://planificacion.cenditel.gob.ve/trac/
"""
## @package django_topic_explorer.utils
#
# Método para crea los archivos copus.dat y vocab.txt
# @author Jorge Redondo (jredondo at cenditel.gob.ve)
# @author <a href='http://www.cenditel.gob.ve'>Centro Nacional de Desarrollo e Investigación en Tecnologías Libres
# (CENDITEL) nodo Mérida - Venezuela</a>
# @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
# @version 1.3
from vsm.extensions.corpusbuilders import dir_corpus
from vsm.extensions.interop.ldac import export_corpus
import sys

def corpus_script(path_corpus,path_output):
	"""!
	Función para construir los archivos del lda
	
	@author Jorge Redondo (jredondo at cenditel.gob.ve)
	@copyright GNU/GPLv2
	@param path_corpus Recibe la ruta donde esta ubicado el corpus
	@param path_output Recibe la ruta de destino donde es secribirán los archivos
	"""
	corpus_object = dir_corpus(path_corpus)
	export_corpus(corpus=corpus_object, outfolder=path_output, context_type=corpus_object.context_types[0])

if __name__ == '__main__':
	if(len(sys.argv)>2):
		path_corpus = sys.argv[1]
		path_output = sys.argv[2]
		corpus_script(path_corpus,path_output)
	else:
		print "Debe ingresar (2) argumentos a la funcion: path_corpus y path_output"
