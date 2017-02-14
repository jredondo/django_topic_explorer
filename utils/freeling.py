# -*- coding: utf-8 -*-
"""
Sistema de Modelado de Tópicos

Copyleft (@) 2014 CENDITEL nodo Mérida - https://planificacion.cenditel.gob.ve/trac/
"""
## @package django_topic_explorer.utils
#
# Métodos utilizados para realizar el pre-procesamiento
# @author Jorge Redondo (jredondo at cenditel.gob.ve)
# @author <a href='http://www.cenditel.gob.ve'>Centro Nacional de Desarrollo e Investigación en Tecnologías Libres
# (CENDITEL) nodo Mérida - Venezuela</a>
# @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
# @version 1.3
from subprocess import Popen, PIPE
import shlex, os
from codecs import open
from nltk.corpus import stopwords
import math, operator

def files_to_lower(path_orig,path_dest):
    """!
    Función para convertir los archivos a sólo letras minusculas
    
    @author Jorge Redondo (jredondo at cenditel.gob.ve)
    @copyright GNU/GPLv2
    @param path_orig Ruta de Origen
    @param path_dest Ruta de Destino
    """
    files = os.listdir(path_orig)
    for file in files:
        file_string = open(path_orig+file,'r','utf8').read()
        f = open(path_dest+file,'w','utf8')
        f.write(file_string.lower())
        f.close()

#os.environ['FREELINGSHARE'] = '/home/jredondo/Proyectos/Analisis_del_Discurso/src/freeling/share/freeling'

#Ruta de la librería del freeling
os.environ['FREELINGSHARE'] = '/usr/local/share/freeling'
def call_freeling(freeling_cmd,file_string):
    """!
    Función para llamar al proceso del freeling
    
    @author Jorge Redondo (jredondo at cenditel.gob.ve)
    @copyright GNU/GPLv2
    @param freeling_cmd Recibe el subproceso a ejecutar
    @param file_string Recibe el contenido del archivo
    @return output Retorna la salida del subproceso
    """
    p = Popen(freeling_cmd, stdin=PIPE, stdout=PIPE, stderr=PIPE)
    output, err = p.communicate(file_string.encode('utf8'))
    print output

    if err < 0:
        return "ERROR: FALLÓ EJECUCIÓN DE FREELING" 

    return output

def clean_words(w):
    """!
    Función para limpiar la palabra de caracteres molestos
    
    @author Jorge Redondo (jredondo at cenditel.gob.ve)
    @copyright GNU/GPLv2
    @param w Recibe la palabra
    @return w Retorna la palabra limpia
    """
    w = w.encode('unicode-escape')
    return w.replace(u'\xe0'.encode('unicode-escape'),u'a').replace(u'\xe8'.encode('unicode-escape'),u'e').replace(u'\xec'.encode('unicode-escape'),u'i').replace(u'\xf2'.encode('unicode-escape'),u'o').replace(u'\xfa'.encode('unicode-escape'),u'u').replace(u'\xe1'.encode('unicode-escape'),u'a').replace(u'\xe9'.encode('unicode-escape'),u'e').replace(u'\xed'.encode('unicode-escape'),u'i').replace(u'\xf3'.encode('unicode-escape'),u'o').replace(u'\xfa'.encode('unicode-escape'),u'u').replace(u'á',u'a').replace(u'é',u'e').replace(u'í',u'i').replace(u'ó',u'o').replace(u'ú',u'u').replace(u'à',u'a').replace(u'è',u'e').replace(u'ì',u'i').replace(u'ò',u'o').replace(u'ù',u'u').decode('unicode-escape')

def is_pos(word,pos_list):
    """!
    Función para comparar si una palabra esta en una lista
    
    @author Jorge Redondo (jredondo at cenditel.gob.ve)
    @copyright GNU/GPLv2
    @param word Recibe la palabra
    @param pos_list Recibe la lista con las palabras
    @return Si la palabra esta en la lista retorna Verdadero, en caso contrario retorna Falso
    """
    for item in pos_list:
        if word.startswith(item): return True
    return False

def complete_word(words_list,word):
    indexes = [i for i,j in enumerate(words_list) if j == word]
    if len(indexes) == 1: return word
    if len(indexes) == 0: return word

    index = 1
    complete_word = word
    i1 = indexes[0]
    while True:
        for i2 in indexes[1:]:
            try:
                if words_list[i1+index] != words_list[i2+index]:
                    return complete_word
            except IndexError:
                return complete_word 
        complete_word += '-' + words_list[i1+index]        
        index += 1
        if indexes[1] == i1+index or i1+index == len(words_list): 
            return complete_word

def all_complete_words(words_list):
    """!
    Función para remover STOPWORDS y caracteres no deseados
    
    @author Jorge Redondo (jredondo at cenditel.gob.ve)
    @copyright GNU/GPLv2
    @param words_list Recibe la lista de las palabras
    @return Las palabras pre-procesadas
    """
    words_list = [w for w in words_list]
    ret_val = []
    c = ''.encode('utf8')
    for w in words_list:
        c_aux = complete_word(words_list,w)
        if c_aux in c:
            continue

        c = c_aux
        ret_val += [c]
    return list(set(ret_val))



def select_pos(path,words_fl,pos_list=['V','A','N','R','D','P','C','I','S']):
    """!
    Función que crea los corpus sin acentos y demás excluye verbos, adjetivos, sutantivos, etc
    
    @author Jorge Redondo (jredondo at cenditel.gob.ve)
    @copyright GNU/GPLv2
    @param path Recibe la palabra
    @param words_fl Recibe las palabras resultantes del freeling
    @param pos_list Recibe los elementos a tomar en cuenta
    @return output_list Retorna una lista con las palabras limpias (sin acentos)
    """
    output_list = []
    all_words_list = []
    for item in words_fl.split('\n'):
        try:
            w = item.split(' ')[0] 
            cleaned_word = clean_words(w.decode('utf8'))
            all_words_list += [cleaned_word]
            if w.decode('utf8') not in stopwords.words('spanish') and is_pos(item.split(' ')[2],pos_list) and w not in '*+.,?¿!¡":;-=/$@#“”()[]{}' and not w.isdigit() and len(w) > 3:
                # Selecciona el lema
                #output_list += [item.split(' ')[1]]
                # Selecciona la palabra original
                #output_list += [item.split(' ')[0]]
                output_list += [cleaned_word]
        except IndexError:
            pass
    na_file = open(path,'w','utf8')
    na_file.write(' '.join(all_words_list))
    na_file.close()
    return output_list 

def preprocess(corpus_path,do_fl=True,pos_list = ['V','A','N','R','D','P','C','I','S']):
    """!
    Función para realizar el pre-procesamiento
    
    @author Jorge Redondo (jredondo at cenditel.gob.ve)
    @copyright GNU/GPLv2
    @param corpus_path Recibe la ruta del corpus
    @param do_fl Recibe la opcion del preprocesamiento (True si se quiere ejecutar, False en caso contrario)
    @return ret_val Retorna un diccionario de los archivos preprocesados
    @return set(corpus_words) Retorna un diccionario con las palabras del corpus preprocesados
    """
    freeling_corpus_path = corpus_path + '../freeling/'
    no_accent_path = corpus_path + '../noaccent/'
    ret_val = dict()
    corpus_words = []
    i = 0
    for file in os.listdir(corpus_path):
        file_string = open(corpus_path+file,'r','utf8').read()
        if do_fl:
            ## Comando por consola que ejecutará el freeling
            freeling_cmd = shlex.split('/usr/local/bin/analyzer -f /usr/local/share/freeling/config/es.cfg',' ')
            # Lematización con FREELING
            words_fl = call_freeling(freeling_cmd,file_string)
            fl_file = open(freeling_corpus_path+file,'w','utf8')
            fl_file.write(words_fl.decode('utf-8'))
            fl_file.close()
        else:
            words_fl = open(freeling_corpus_path+file,'r').read()
        ####################################
        ####################################
        #'V', verbos
        #'A', adjetivos
        #'N', sustantivos
        #'R', adverbios
        #'D', determinantes
        #'P', pronombres     
        #'C', conjunciones
        #'I', interjecciones
        #'S', preposiciones
        ####################################
        ####################################

        words_fl = select_pos(no_accent_path+file,words_fl=words_fl,pos_list=pos_list)

        # Quitar STOPWORDS y caracteres no deseados
        words_pp = all_complete_words(words_fl)
        ret_val[file] = words_pp
        corpus_words += words_pp
        i += 1

    return ret_val,set(corpus_words)

def idf(file_words_pp,corpus_words):
    idf = {}
    num_docs = len(file_words_pp)
    for w in corpus_words:
        count = 0
        for file,words in file_words_pp.items():
            if w in words: count += 1
        idf[w] = math.log(float(num_docs)/float(1+count))
    return idf

def generate_exluded_file(corpus_path,pp_corpus_path,file_words_pp,exclude_words):
    """!
    Función que generra el archivo de palabras excluidas
    
    @author Jorge Redondo (jredondo at cenditel.gob.ve)
    @copyright GNU/GPLv2
    @param corpus_path Recibe la ruta del corpus
    @param pp_corpus_path Recibe la ruta de los archivos pre-procesados
    @param file_words_pp Recibe los archivos pre-procesados
    @param exclude_words Recibe la lista con las palabras excluidas
    """
    excluded = open(corpus_path+'excluded.txt','w','utf8')
    added_files = []
    repeated_count = 0
    flag = False
    for file,words_pp in file_words_pp.items():
        # Excluir documentos repetidos
        for aux_words_pp in added_files:
            if words_pp == aux_words_pp:
                repeated_count += 1
                print "Repetido: " + file
                flag = True
                break
        if flag:
            flag = False
            continue
             
        if len(words_pp) <= 50: continue
        # Guardar archivo 
        file_pp = open(pp_corpus_path+file,'w','utf8')
        added_files.append(words_pp)
        for w in words_pp:
            if w not in exclude_words and not '_' in w:
                file_pp.write(w + ' ')
            else:
                try:
                    excluded.write(w.encode('utf8') + ' (' + file + ')\n')
                except UnicodeDecodeError:
                    excluded.write(w + ' (' + file + ')\n')
        file_pp.close()
    excluded.close()

 
if __name__ == '__main__':
    
    ## Ruta donde se encuentra el corpus
    corpus_path = '/home/rodrigo/Proyectos/Interpretacion/demo-data/corta/'
    orig_corpus_path = corpus_path + 'orig/'
    lower_corpus_path = corpus_path + 'lower/'
    pp_corpus_path = corpus_path + 'pp/'
    
    ## Crea los archivos de puro minusculas
    files_to_lower(orig_corpus_path,lower_corpus_path)
    
    ## Se realiza el pre-procesamiento
    file_words_pp,corpus_words = preprocess(lower_corpus_path,do_fl=True,pos_list=['A','R','V','N'])
    ## Palabras a excluir
    exclude_words = ['descripcion','justificacion','construccion','desarrollo','comunidad','comunal','proyecto','prueblo','desarrollar','mismo','nacional','pueblo','sistema','año','años']
    ## Se decodifican las ñ
    other_words = [x.decode('utf8') for x in exclude_words]
    ## Se genera el archivo de vocabulario excluido
    generate_exluded_file(corpus_path,pp_corpus_path,file_words_pp,other_words)
   

