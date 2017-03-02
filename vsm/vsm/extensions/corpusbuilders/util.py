import re

from chardet.universaldetector import UniversalDetector
import nltk
import numpy as np

__all__ = ['strip_punc', 'rem_num', 'rehyph',
           'apply_stoplist', 'filter_by_suffix', 'word_tokenize',
           'sentence_tokenize', 'paragraph_tokenize', 'detect_encoding']



def strip_punc(tsent):
    """
    """
    p1 = re.compile(r'^([^a-zA-Z0-9]*)')
    p2 = re.compile(r'([^a-zA-Z0-9]*)$')

    out = []
    for word in tsent:
        w = re.sub(p2, '', re.sub(p1, '', word))
        if w:
            out.append(w)

    return out


def rem_num(tsent):
    """
    """
    p = re.compile(r'(^\D+$)|(^\D*[1-2]\d\D*$|^\D*\d\D*$)')

    return [word for word in tsent if re.search(p, word)]


def rehyph(sent):
    """
    """
    return re.sub(r'(?P<x1>.)--(?P<x2>.)', '\g<x1> - \g<x2>', sent)


def apply_stoplist(corp, nltk_stop=True, add_stop=None, freq=0):
    """
    Returns a Corpus object with stop words eliminated.

    :param corp: Corpus object to apply stoplist to.
    :type corp: Corpus

    :param nltk_stop: If `True` English stopwords from nltk are included
        in the stoplist. Default is `True`.
    :type nltk_stop: boolean, optional
    
    :param add_stop: list of words to eliminate from `corp` words.
        Default is `None`.
    :type add_stop: List, optional

    :param freq: Eliminates words that appear <= `freq` times. Default is
        0.
    :type freq: int

    :returns: Corpus with words in the stoplist removed.

    :See Also: :class:`vsm.corpus.Corpus`, :meth:`vsm.corpus.Corpus.apply_stoplist`
    """
    stoplist = set()
    if nltk_stop:
        for w in nltk.corpus.stopwords.words('english'):
            stoplist.add(w)
    if add_stop:
        for w in add_stop:
            stoplist.add(w)

    return corp.apply_stoplist(stoplist=stoplist, freq=freq)


def filter_by_suffix(l, ignore, filter_dotfiles=True):
    """
    Returns elements in `l` that does not end with elements in `ignore`,
    and filters dotfiles (files that start with '.').

    :param l: List of strings to filter.
    :type l: list

    :param ignore: List of suffix to be ignored or filtered out.
    :type ignore: list

    :param filter_dotfiles: Filter dotfiles.
    :type filter_dotfiles: boolean, default True

    :returns: List of elements in `l` whose suffix is not in `ignore`.

    **Examples**

    >>> l = ['a.txt', 'b.json', 'c.txt']
    >>> ignore = ['.txt']
    >>> filter_by_suffix(l, ignore)
    ['b.json']
    """
    filter_list = [e for e in l if not sum([e.endswith(s) for s in ignore])]
    if filter_dotfiles:
        filter_list = [e for e in filter_list if not e.startswith('.')]
    return filter_list


def word_tokenize(text):
    """Takes a string and returns a list of strings. Intended use: the
    input string is English text and the output consists of the
    lower-case words in this text with numbers and punctuation, except
    for hyphens, removed.

    The core work is done by NLTK's Treebank Word Tokenizer.
    
    :param text: Text to be tokeized.
    :type text: string

    :returns: tokens : list of strings
    """

    text = rehyph(text)
    text = nltk.TreebankWordTokenizer().tokenize(text)

    tokens = [word.lower() for word in text]
    tokens = strip_punc(tokens)
    tokens = rem_num(tokens)
    
    return tokens


def sentence_tokenize(text):
    """
    Takes a string and returns a list of strings. Intended use: the
    input string is English text and the output consists of the
    sentences in this text.

    This is a wrapper for NLTK's pre-trained Punkt Tokenizer.
     
    :param text: Text to be tokeized.
    :type text: string

    :returns: tokens : list of strings
    """
    tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')

    return tokenizer.tokenize(text)


def paragraph_tokenize(text):
    """
    Takes a string and returns a list of strings. Intended use: the
    input string is English text and the output consists of the
    paragraphs in this text. It's expected that the text marks
    paragraphs with two consecutive line breaks.
     
    :param text: Text to be tokeized.
    :type text: string

    :returns: tokens : list of strings
    """

    par_break = re.compile(r'[\r\n]{2,}')
    
    return par_break.split(text)


def detect_encoding(filename):
    """
    Takes a filename and attempts to detect the character encoding of the file
    using `chardet`.
     
    :param filename: Name of the file to process
    :type filename: string

    :returns: encoding : string
    """
    detector = UniversalDetector()
    with open(filename, 'rb') as unknown_file:
        for line in unknown_file:
            detector.feed(line)
            if detector.done:
                break
    detector.close()

    return detector.result['encoding']
     
