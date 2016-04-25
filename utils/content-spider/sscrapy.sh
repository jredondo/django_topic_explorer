#!/bin/bash 

#La variable IFS (Internal Field Separator) es una variable de entorno que sirve para indicar al intérprete bash cómo debe reconocer los campos en una cadena de caracteres. 
#Por defecto el separador es el espacio en blanco (tabuladores y saltos de linea incluidos).

rm *.json

scrapy crawl el_nacional -o elnacional.json
scrapy crawl el_universal -o eluniversal.json
scrapy crawl la_patilla -o lapatilla.json
scrapy crawl dolar_today -o dolartoday.json
scrapy crawl noticias24 -o noticias24.json
scrapy crawl talcual -o talcual.json
scrapy crawl venevision -o venevision.json
scrapy crawl globovision -o globovision.json
scrapy crawl noticiero_digital -o noticierodigital.json
scrapy crawl la_verdad -o laverdad.json
scrapy crawl informe21 -o informe21.json
scrapy crawl quinto_dia -o quintodia.json
scrapy crawl 2001 -o 2001.json
scrapy crawl ultimas_noticias -o ultimasnoticias.json
scrapy crawl noticias_vzla -o noticiasvzla.json
scrapy crawl elcarabobeno -o elcarabobeno.json
scrapy crawl unbombazo -o unbombazo.json
scrapy crawl caraota_digital -o caraotadigital.json

echo Script finalizado
