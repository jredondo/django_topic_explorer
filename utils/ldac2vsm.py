from vsm.extensions.interop.ldac import import_corpus
from vsm.extensions.corpusbuilders import dir_corpus
from vsm.corpus import Corpus
from vsm.model.ldacgsmulti import LdaCgsMulti

from vsm.model.ldafunctions import *
import math
import numpy as np


path = '/home/jredondo/Proyectos/Analisis_del_Discurso/src/lda-blei/lda-c-dist/output/'
#corpus_file = '/home/jredondo/Proyectos/Analisis_del_Discurso/src/vsm_tmp/corpus.dat'
corpus_file = '/home/jredondo/Proyectos/Analisis_del_Discurso/src/lda-blei/ap/ap.dat'
vocab_file = '/home/jredondo/Proyectos/Analisis_del_Discurso/src/lda-blei/ap/vocab.txt'

def likelihood(path=path):
  with open(path + 'likelihood.dat') as f:
    lh = f.readlines()
  return np.array([item.strip('\n').split('\t')[0] for item in lh],dtype=np.float)

def beta(path=path):
  b = []
  with open(path + 'final.beta') as f:
    for line in f:
      b.append([math.exp(float(item)) for item in line.strip('\n').split()])
      #b.append([10**float(item) for item in line.strip('\n').split()])
  return b


def alpha(path=path):
  with open(path + 'final.other') as f:
    a = f.readlines()
  return float(a[2].split()[1])

def word_assigments(path=path):
  indices_tmp = []
  z_tmp = []
  with open(path + 'word-assignments.dat') as f:
    for line in f:
      indices_tmp += [int(line.strip('\n').split()[0])]
      line_split = line.strip('\n').split()
      z_tmp.append(line_split[1:len(line_split)])
  indices = []
  for i in xrange(len(indices_tmp)):
    indices += [sum(indices_tmp[0:i+1])]

  z = list(range(len(z_tmp)))
  for i,doc in enumerate(z_tmp):
    z[i] = [int(item.split(':')[1]) for item in doc]
  
  return z,indices

def corpus(file=corpus_file):
  with open(file) as f:
    c = f.readlines()
  indices_tmp = [int(item.strip('\n').split()[0]) for item in c]
  indices = []
  for i in xrange(len(indices_tmp)):
    indices += [sum(indices_tmp[0:i+1])]

  c_tmp = [item.strip('\n').split()[1:len(item.strip('\n').split())] for item in c]
  c = list(range(len(c_tmp)))
  for i,doc in enumerate(c_tmp):
    c[i] = [int(item.split(':')[0]) for item in doc]

  return c,indices

def vocab(file=vocab_file):
  with open(file) as f:
    v = f.readlines()
  return len(v)

def alpha_list(z,path=path):
  a = alpha(path)
  a_list = []
  for i in range(len(z)):
    a_list += [a]
  return a_list 


def top_doc(path=path):
  z,indices = word_assigments(path)
  b = beta(path)
  a_list = alpha_list(z,path)
  return compute_top_doc(z, len(b), np.array(a_list))
   
def word_top(path=path):
  c,indices = corpus()
  z,indices = word_assigments(path)
  b = beta(path)
  v = vocab()
  return compute_word_top(c, z, len(b), v, np.transpose(b))
 
def log_prob(path=path): 
  wt =  word_top(path)
  td = top_doc(path)
  c,indices = corpus()
  z,indices = word_assigments(path)
  return compute_log_prob(c, z, wt, td)
 
if __name__=='__main__':

  z,indices = word_assigments(path)
  b = beta(path)
  v = vocab()
  a = alpha_list(z,path)
  c = import_corpus(corpus_file,vocab_file) 
  m = LdaCgsMulti(corpus=c,K=20,V=v,alpha=a,beta=b)

