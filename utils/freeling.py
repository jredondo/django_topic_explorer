# coding: utf8
from subprocess import Popen, PIPE
import shlex, os
from codecs import open
from nltk.corpus import stopwords
import math, operator


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

    return output


def clean_words(words_fl):
    words_fl = [w.encode('unicode-escape') for w in words_fl]
    return [w.replace(u'\xe0'.encode('unicode-escape'),u'a').replace(u'\xe8'.encode('unicode-escape'),u'e').replace(u'\xec'.encode('unicode-escape'),u'i').replace(u'\xf2'.encode('unicode-escape'),u'o').replace(u'\xfa'.encode('unicode-escape'),u'u').replace(u'\xe1'.encode('unicode-escape'),u'a').replace(u'\xe9'.encode('unicode-escape'),u'e').replace(u'\xed'.encode('unicode-escape'),u'i').replace(u'\xf3'.encode('unicode-escape'),u'o').replace(u'\xfa'.encode('unicode-escape'),u'u').replace(u'á',u'a').replace(u'é',u'e').replace(u'í',u'i').replace(u'ó',u'o').replace(u'ú',u'u').replace(u'à',u'a').replace(u'è',u'e').replace(u'ì',u'i').replace(u'ò',u'o').replace(u'ù',u'u') for w in words_fl if w not in stopwords.words('spanish') and w not in '*+.,?¿!¡":;-=/$@#“”()[]{}' and not w.isdigit() and len(w) > 3]

def is_pos(word,pos_list):
    for item in pos_list:
        if word.startswith(item): return True
    return False

def complete_word(words_list,word):
    indexes = [i for i,j in enumerate(words_list) if j == word]
    if len(indexes) == 1: return word
    if len(indexes) == 0: return word

    #if len(indexes) == 0: raise Exception("LA PALABRA NO SE ENCUENTRA EN EL DOCUMENTO: cosa rara!")
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
    words_list = [w.decode('utf8') for w in words_list]
    ret_val = []
    c = ''.encode('utf8')
    for w in words_list:
        c_aux = complete_word(words_list,w)
        if c_aux in c:
            continue

        c = c_aux
        ret_val += [c]
    return list(set(ret_val))



def select_pos(words_fl,pos_list=['V','A','N','R','D','P','C','I','S']):
    output_list = []
    for item in words_fl.split('\n'):
        try:
            if item.split(' ')[0].decode('utf8') not in stopwords.words('spanish') and is_pos(item.split(' ')[2],pos_list):
                # Selecciona el lema
                #output_list += [item.split(' ')[1]]
                # Selecciona la palabra original
                output_list += [item.split(' ')[0]]
        except IndexError:
            pass
    return output_list 


def preprocess(corpus_path,do_fl=True):
    freeling_cmd = shlex.split('/home/jredondo/Proyectos/Analisis_del_Discurso/src/freeling/bin/analyzer -f /home/jredondo/Proyectos/Analisis_del_Discurso/src/freeling/share/freeling/config/es.cfg',' ')
    freeling_corpus_path = corpus_path + '../freeling/'
    ret_val = dict()
    corpus_words = []
    i = 0
    for file in os.listdir(corpus_path):
        file_string = open(corpus_path+file,'r','utf8').read()
        if do_fl:
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
        #'R', advervios
        #'D', determinantes
        #'P', pronombres     
        #'C', conjunciones
        #'I', interjecciones
        #'S', preposiciones
        words_fl = select_pos(words_fl=words_fl,pos_list=['A','R','V','N'])
        ####################################
        ####################################
        # Quitar STOPWORDS y caracteres no deseados
        words_pp = all_complete_words(words_fl)
        words_pp = clean_words(words_pp)
        ret_val[file] = words_pp
        corpus_words += words_pp
        i += 1
        #print "Pre-procesado el archivo: " + file
        #print "####################################"
        #print words_pp , '(' + str(i) + ')'
        #print "####################################"
        #print "####################################"

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
 
    file_words_pp,corpus_words = preprocess(lower_corpus_path,do_fl=False) 
    exclude_words = ['descripcion','justificacion','construccion','desarrollo','comunidad','comunal','proyecto','prueblo','desarrollar','mismo','nacional','pueblo','sistema']
    exclude_words = [w.encode('utf8') for w in exclude_words]
    #vocab_idf = idf(file_words_pp,corpus_words)
    #print sorted(vocab_idf.items(),key=operator.itemgetter(1), reverse=True)
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
             
        #coef = float(len(set(words_pp)))/float(len(words_pp))
        #print coef, len(words_pp), file
        #if (coef <= 0.5) or len(words_pp) <= 150: continue
        if len(words_pp) <= 50: continue
        # Guardar archivo 
        file_pp = open(pp_corpus_path+file,'w','utf8')
        added_files.append(words_pp)
        for w in words_pp:
            #condition = vocab_idf[w]
            #if condition >= 2.0 and condition <= 6.1 and not '_' in w:
            #if condition >= 2.0 and not '_' in w:
        
            if w not in exclude_words and not '_' in w:

                #try:
                #    file_pp.write(w.encode('utf8') + ' ')
                #except UnicodeDecodeError:
                file_pp.write(w + ' ')
            else:
                try:
                    #excluded.write(w.encode('utf8') + ' ' + str(condition) + ' (' + file + ')\n')
                    excluded.write(w.encode('utf8') + ' (' + file + ')\n')
                except UnicodeDecodeError:
                    #excluded.write(w + ' ' + str(condition) + ' (' + file + ')\n')
                    excluded.write(w + ' (' + file + ')\n')
        file_pp.close()
    excluded.close()
   
    print "Documentos repetidos: ", repeated_count
    print "Palabras en el vocabulario: ", len(corpus_words)
