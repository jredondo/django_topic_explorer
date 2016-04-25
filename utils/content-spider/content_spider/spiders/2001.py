import scrapy

from utils import *
from settings import settings

class SiteSpySpider(scrapy.Spider):
	
	name = "2001"
	start_urls = [settings[name]['url']]		
	
	def parse(self, response):
		for href in response.css(settings[self.name]['links']):
			full_url = response.urljoin(href.extract())
			yield scrapy.Request(full_url, callback=self.parse_links)	
						
	def parse_links(self, response):
		fecha = response.css(settings[self.name]['fecha']).extract()[-1]
		current_date = obtener_fecha_tipo10(fecha)
		if(current_date):
			body = limpiar_quintodia(response.css(settings[self.name]['body']).extract())
			if(body!=''):
				yield {
				'titulo': response.css(settings[self.name]['titulo']).extract()[0],
				'autor': '',
				'fecha': fecha,
				'body': [body],
				'link': response.url,
				}
