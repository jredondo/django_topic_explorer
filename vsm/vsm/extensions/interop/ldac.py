"""
vsm.extensions.interop.ldac

Module containing functions for import/export between VSM and lda-c, which is
the original LDA implementation referenced in Blei, Ng, and Jordan (2003). 
lda-c is available at: http://www.cs.princeton.edu/~blei/lda-c/
"""
import os, os.path
import codecs

from scipy.stats import itemfreq
import numpy as np

from vsm.extensions.corpusbuilders import corpus_fromlist

def export_corpus(corpus, outfolder, context_type='document'):
    """
    Converts a vsm.corpus.Corpus object into a lda-c compatible data file.
    Creates two files:
    1.  "vocab.txt" - contains the integer-word mappings
    2.  "corpus.dat" - contains the corpus object in the format described in 
        [lda-c documentation](http://www.cs.princeton.edu/~blei/lda-c/readme.txt):

            Under LDA, the words of each document are assumed exchangeable.  Thus,
            each document is succinctly represented as a sparse vector of word
            counts. The data is a file where each line is of the form:
        
                [M] [term_1]:[count] [term_2]:[count] ...  [term_N]:[count]
        
            where [M] is the number of unique terms in the document, and the
            [count] associated with each term is how many times that term appeared
            in the document.  Note that [term_1] is an integer which indexes the
            term; it is not a string.

    :param corpus: VSM Corpus object to convert to lda-c file
    :type corpus: vsm.corpus.Corpus

    :param outfolder: Directory to output "vocab.txt" and "corpus.dat"
    :type string: path
    """
    if not os.path.exists(outfolder):
        os.makedirs(outfolder)

    vocabfilename = os.path.join(outfolder, 'vocab.txt')
    with codecs.open(vocabfilename,'w','utf8') as vocabfile:
        for word in corpus.words:
            vocabfile.write(word+'\n')

    corpusfilename = os.path.join(outfolder, 'corpus.dat')
    corpusitemnames = os.path.join(outfolder,'names.dat')

    #print "METADATA",len(corpus.view_metadata(context_type))
    #print len(corpus.view_contexts(context_type))
    #vw_ctx = corpus.view_contexts(context_type)
    #vw_mtd = corpus.view_metadata(context_type)
    #for i,item in enumerate(vw_mtd):
    #    if i < 1: 
    #        print vw_mtd[i][1],vw_mtd[i][0],len(vw_ctx[i])
    #    else:
    #        print vw_mtd[i][1], vw_mtd[i][0]-vw_mtd[i-1][0],len(vw_ctx[i])


    #vw_mtd = corpus.view_metadata(context_type)
    #names_file = open(corpusitemnames,'w')
    with open(corpusfilename,'w') as corpusfile:
        for i,ctx in enumerate(corpus.view_contexts(context_type)):
            M = len(np.unique(ctx))
            corpusfile.write("{0}".format(M))
            #names_file.write("{0} {1}\n".format(vw_mtd[i][1],vw_mtd[i][0]))

            for token in itemfreq(ctx):
                corpusfile.write(" {term}:{count}".format(
                    term=token[0],count=token[1]))

            corpusfile.write("\n")
        #names_file.close()

def import_corpus(corpusfilename, vocabfilename, context_type='document', path=None):
    """
    Converts an lda-c compatible data file into a VSM Corpus object.

    :param corpusfilename: path to corpus file, as defined in lda-c
    documentation.
    :type string:

    :param vocabfilename: path to vocabulary file, one word per line
    :type string:
    """
    # process vocabulary file 
    with codecs.open(vocabfilename,'r','utf8') as vocabfile:
        vocab = [line.strip() for line in vocabfile]

    # process corpus file
    corpus = []
    with codecs.open(corpusfilename,'r','utf8') as corpusfile:
        for line in corpusfile:
            tokens = line.split()[1:]
            ctx = []
            for token in tokens:
                id, count = token.split(':')
                id = int(id)
                count = int(count)
                ctx.extend([vocab[id]] * count)
            corpus.append(ctx)

    if path:
        files_names = [file for file in os.listdir(path)]
       
    return corpus_fromlist(corpus, files_names, context_type=context_type)

def import_model(filename):
    pass
def export_model(filename):
    pass
