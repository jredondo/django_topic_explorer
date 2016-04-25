import scrapy

from utils import *
from settings import settings

class SiteSpySpider(scrapy.Spider):
	
	name = "talcual"
	start_urls = [settings[name]['url']]		
	
	def parse(self, response):
		for href in response.css(settings[self.name]['links']):
			full_url = response.urljoin(href.extract())
			yield scrapy.Request(full_url, callback=self.parse_links)	
						
	def parse_links(self, response):
		if(not('Autor/' in response.url)):
			fecha = response.css(settings[self.name]['fecha']).extract()[0]
			current_date = obtener_fecha_tipo6(fecha)
			if(current_date):
				body = limpiar(response.css(settings[self.name]['body']).extract());
				autor = limpiar_autor_tc(response.css(settings[self.name]['autor']).extract()[0])
				if(body!=''):
					yield {
					'titulo': response.css(settings[self.name]['titulo']).extract()[0],
					'autor': autor,
					'fecha': fecha,
					'body': [body],
					'link': response.url,
					}
