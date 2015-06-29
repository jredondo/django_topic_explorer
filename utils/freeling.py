# coding: utf8
from subprocess import Popen, PIPE
import shlex, os
from codecs import open
from nltk.corpus import stopwords
import math


def files_to_lower(path_orig,path_dest):
    files = os.listdir(path_orig)
    for file in files:
        file_string = open(path_orig+file,'r','utf8').read()
        f = open(path_dest+file,'w','utf8')
        f.write(file_string.lower())
        f.close()

os.environ['FREELINGSHARE'] = '/home/jredondo/Proyectos/Analisis_del_Discurso/src/freeling/share/freeling'
def call_freeling(freeling_cmd,file_string):
    p = Popen(freeling_cmd, stdin=PIPE, stdout=PIPE, stderr=PIPE)
    output, err = p.communicate(file_string.encode('utf8'))

    if err < 0:
        return "ERROR: FALLÓ EJECUCIÓN DE FREELING" 

    output_list = []
    for item in output.split('\n'):
        if item.split(' ')[0] not in stopwords.words('spanish'):
            try:
                output_list += [item.split(' ')[1]]
            except IndexError:
                pass
    return output_list 

def clean_words(words_fl):
    return [w.decode('utf8').replace(u'á',u'a').replace(u'é',u'e').replace(u'í',u'i').replace(u'ó',u'o').replace(u'ú',u'u').replace(u'à',u'a').replace(u'è',u'e').replace(u'ì',u'i').replace(u'ò',u'o').replace(u'ù',u'u') for w in words_fl if w.decode('utf8') not in stopwords.words('spanish') and w.decode('utf8') not in '*+.,?¿!¡":;-=/$@#“”()[]{}'.decode('utf8') and not w.decode('utf8').isdigit() and len(w) > 3]
 
def preprocess(corpus_path):
    freeling_cmd = shlex.split('/home/jredondo/Proyectos/Analisis_del_Discurso/src/freeling/bin/analyzer -f /home/jredondo/Proyectos/Analisis_del_Discurso/src/freeling/share/freeling/config/es.cfg',' ')
    freeling_corpus_path = corpus_path + 'freeling/'
    ret_val = dict()
    corpus_words = []
    i = 0
    for file in os.listdir(corpus_path):
        file_string = open(corpus_path+file,'r','utf8').read()
        # Lematización con FREELING
        words_fl = call_freeling(freeling_cmd,file_string)
        # Quitar STOPWORDS y caracteres no deseados
        words_pp = clean_words(words_fl)
        ret_val[file] = words_pp
        corpus_words += words_pp
        i += 1
        print "Pre-procesado el archivo: " + file
        print "####################################"
        print words_pp , '(' + str(i) + ')'
        print "####################################"
        print "####################################"

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

 
if __name__ == '__main__':
    """
    path_orig = '/home/jredondo/Proyectos/Analisis_del_Discurso/src/topic-explorer/demo-data/corpus_propuestas/orig/'
    path_dest = '/home/jredondo/Proyectos/Analisis_del_Discurso/src/topic-explorer/demo-data/corpus_propuestas/lower/'
    files_to_lower(path_orig,path_dest)
    """
    corpus_path = '/home/jredondo/Proyectos/Analisis_del_Discurso/src/topic-explorer/demo-data/corpus_propuestas/'
    lower_corpus_path = corpus_path + 'lower/'
    pp_corpus_path = corpus_path + 'pp/'
 
    file_words_pp,corpus_words = preprocess(lower_corpus_path) 
    vocab_idf = idf(file_words_pp,corpus_words)
    excluded = open(corpus_path+'excluded.txt','w','utf8')
    for file,words_pp in file_words_pp.items():
        # Guardar archivo 
        file_pp = open(pp_corpus_path+file,'w','utf8')
        for w in words_pp:
            condition = vocab_idf[w]
            if condition >= 1.2 and condition <= 6.1 and not '_' in w:
                try:
                    file_pp.write(w.encode('utf8') + ' ')
                except UnicodeDecodeError:
                    file_pp.write(w + ' ')
            else:
                try:
                    excluded.write(w.encode('utf8') + ' ' + str(condition) + ' (' + file + ')\n')
                except UnicodeDecodeError:
                    excluded.write(w + ' ' + str(condition) + ' (' + file + ')\n')
        file_pp.close()
    excluded.close()
   
    print "Palabras en el vocabulario: ", len(corpus_words)
