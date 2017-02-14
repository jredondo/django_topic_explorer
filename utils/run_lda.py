# -*- coding: utf-8 -*-
"""
Sistema de Modelado de Tópicos

Copyleft (@) 2014 CENDITEL nodo Mérida - https://planificacion.cenditel.gob.ve/trac/
"""
## @package django_topic_explorer.utils
#
# Métodos para correr el lda
# @author Rodrigo Boet (rboet at cenditel.gob.ve)
# @author <a href='http://www.cenditel.gob.ve'>Centro Nacional de Desarrollo e Investigación en Tecnologías Libres
# (CENDITEL) nodo Mérida - Venezuela</a>
# @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
# @version 1.3
from subprocess import Popen

def call_lda(command):
    """!
    Función para llamar al proceso del LDA
    
    @author Rodrigo Boet (rboet at cenditel.gob.ve)
    @copyright GNU/GPLv2
    @date 09-02-2017
    @param command Recibe el comando a ejecutar
    @return output Retorna la salida del subproceso
    """
    print command
    p = Popen(command)
    
    output, errs = p.communicate()

    if errs < 0:
        return "ERROR: FALLÓ EJECUCIÓN DE LDA" 
    return output


def generate_comand(base_dir,corpus_path,filename,topics_number):
    """!
    Función para generar los procesos del LDA
    
    @author Rodrigo Boet (rboet at cenditel.gob.ve)
    @copyright GNU/GPLv2
    @date 09-02-2017
    @param base_dir Recibe la ruta base
    @param corpus_path Recibe la ruta del corpus.dat
    @param filename Recibe el nombre con el que se generará el directorio
    @param topics_number Recibe el número de tópicos
    """
    settings_path = base_dir+'/utils/lda/settings.txt'
    lda_exe = base_dir+'/utils/lda/lda'
    name = filename.split("/")[-1]
    filename = filename+"/lda/"+name
    for i in range(1,topics_number+1):
        command = "{0} est 0.1 {1} {2} {3} random {4}{1}".format(lda_exe,i*10,settings_path,corpus_path,filename)
        call_lda(command.split(" "))