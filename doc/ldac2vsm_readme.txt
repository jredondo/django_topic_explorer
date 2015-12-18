Integración LDA-c y VSM:
========================

Generar un corpus de entrada para LDA-c (corpus.dat) 
a partir de los archivos contenidos en un directorio, 
cada archivo un texto del corpus:
python corpusScript.py path_corpus path_salida

Algunos adelantos para visualizar en la interfaz 
gráfica los resultados de LDA-c están contenidos
en el script: ldac2vsm.py


Correr LDA-c:
-------------
lda est [initial alpha] [k] [settings] [data] [random/seeded/*] [directory]

Ejemplo:
--------
./lda est 0.1 20 settings.txt corpus.dat random output/

Visualizar salida de LDA-c:
---------------------------
python topics.py <beta-file> <vocab-file> <num words>

Ejemplo:
--------
python topics.py output/final.beta vocab.txt 12

