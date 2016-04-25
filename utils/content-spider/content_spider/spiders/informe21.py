import scrapy

from utils import *
from settings import settings

class SiteSpySpider(scrapy.Spider):
	
	name = "informe21"
	start_urls = [settings[name]['url']]		
	
	def parse(self, response):
		for href in response.css(settings[self.name]['links']):
			full_url = response.urljoin(href.extract())
			yield scrapy.Request(full_url, callback=self.parse_links)	
						
	def parse_links(self, response):
		if (not(('actualidad/' in response.url) or ('salud-y-bienestar/' in response.url) or ('ciencia-y-tecnologia' in response.url) or ('blog' in response.url)
		or ('amor' in response.url) or ('arte-y-espectaculos' in response.url) or ('deportes' in response.url) or ('gastronomia' in response.url)
		or ('www.diosuniversal.com' in response.url))):
			fecha = response.css(settings[self.name]['fecha']).extract()[0]
			current_date = obtener_fecha_orig2(fecha.split(" ")[1])
			if(current_date):
				body = limpiar(response.css(settings[self.name]['body']).extract())
				yield {
				'titulo': response.css(settings[self.name]['titulo']).extract()[0],
				'autor': '',
				'fecha': fecha,
				'body': [body],
				'link': response.url,
				}
