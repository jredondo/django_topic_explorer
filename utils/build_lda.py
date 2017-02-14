# -*- coding: utf-8 -*-
"""
Sistema de Modelado de Tópicos

Copyleft (@) 2014 CENDITEL nodo Mérida - https://planificacion.cenditel.gob.ve/trac/
"""
## @package django_topic_explorer.utils
#
# Métodos para generar los archivos del LDA resultantes de verificar el pre-procesamiento
# @author Jorge Redondo (jredondo at cenditel.gob.ve)
# @author <a href='http://www.cenditel.gob.ve'>Centro Nacional de Desarrollo e Investigación en Tecnologías Libres
# (CENDITEL) nodo Mérida - Venezuela</a>
# @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
# @version 1.3

import glob
import sys

def build_lda(path_corpus,path_output):
  """!
  Función para construir los archivos del lda
  
  @author Jorge Redondo (jredondo at cenditel.gob.ve)
  @copyright GNU/GPLv2
  @param path_corpus Recibe la ruta donde esta ubicado el corpus
  @param path_output Recibe la ruta de destino donde es secribirán los archivos
  """
  
  files = glob.glob(path_corpus+'/*')

  vocab = []
  f_dict = {}
  # To build vocabulary, first
  for f in files:
    # It's supposed that each files has only one line, thus index 0
    f_words = open(f).readlines()[0].split(' ')
    f_words = [w.decode('utf8').strip(u'\ufeff') for w in f_words if len(w) > 0]
    f_dict[f.split('/')[-1]] = f_words
    vocab += f_words

  vocab = sorted(set(vocab))

  with open(path_output+'corpus.dat','w') as outfile:
    for item in f_dict.items():
      outfile.write(str(len(item[1]))+' ')

      for w in set(item[1]):
        outfile.write(str(vocab.index(w)) + ':' + str(item[1].count(w)) + ' ')

      outfile.write('\n')

  with open(path_output+'vocab.txt','w') as outfile:
    for item in vocab:
      outfile.write(item.encode('utf8')+'\n')
    

if __name__ == '__main__':
  if(len(sys.argv)==3):
    path_corpus = sys.argv[1]
    path_output = sys.argv[2]
    build_lda(path_corpus,path_output)
    print "Se ejecutó el comando con éxito"
  else:
    print "Debe ingresar (2) argumentos a la función: path_corpus y path_output"


