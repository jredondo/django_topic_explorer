import scrapy

from utils import *
from settings import settings

class SiteSpySpider(scrapy.Spider):
	
	name = "el_universal"
	start_urls = [settings[name]['url']]		
	
	def parse(self, response):
		for href in response.css(settings[self.name]['links']):
			full_url = response.urljoin(href.extract())
			yield scrapy.Request(full_url, callback=self.parse_links)	
						
	def parse_links(self, response):
		fecha = response.css(settings[self.name]['fecha']).extract()[0]
		current_date = obtener_fecha_tipo2(fecha)
		if (not(('noticias/deportes' in response.url) or ('noticias/beisbol' in response.url) or ('noticias/futbol' in response.url) or ('noticias/cine' in response.url)
		or ('noticias/cultura' in response.url) or ('noticias/caracas' in response.url) or ('noticias/estilo-vida' in response.url) or ('noticias/baloncesto' in response.url)
		or('infografias/deportes' in response.url) or('infografias/estilo-vida' in response.url) or('videos' in response.url) or('galerias' in response.url)
		or('noticias/tecnologia' in response.url) or('noticias/que-hay' in response.url) or('noticias/tenias' in response.url) or('audio' in response.url)) and current_date):
			autor = get_author_eu(response.css(settings[self.name]['autor']).extract())
			body = limpiar_eu([response.css(settings[self.name]['body'][0]).extract(),response.css(settings[self.name]['body'][1]).extract()])
			yield {
			'titulo': response.css(settings[self.name]['titulo']).extract()[0],
			'autor': autor,
			'fecha': fecha,
			'body': [body],
			'link': response.url,
			}
