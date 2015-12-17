from vsm.extensions.corpusbuilders import dir_corpus
from vsm.extensions.interop.ldac import export_corpus
import sys

def corpus_script(path_corpus,path_output):
	corpus_object = dir_corpus(path_corpus)
	export_corpus(corpus=corpus_object, outfolder=path_output, context_type=corpus_object.context_types[0])

if __name__ == '__main__':
	if(len(sys.argv)>2):
		path_corpus = sys.argv[1]
		path_output = sys.argv[2]
		corpus_script(path_corpus,path_output)
	else:
		print "Debe ingresar (2) argumentos a la funcion: path_corpus y path_output"
