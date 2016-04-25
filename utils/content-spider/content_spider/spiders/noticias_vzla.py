import scrapy

from utils import *
from settings import settings

class SiteSpySpider(scrapy.Spider):
	
	name = "noticias_vzla"
	start_urls = [settings[name]['url']]		
	
	def parse(self, response):
		for href in response.css(settings[self.name]['links']):
			full_url = response.urljoin(href.extract())
			yield scrapy.Request(full_url, callback=self.parse_links)	
						
	def parse_links(self, response):
		body = limpiar_not_vzla(response.css(settings[self.name]['body']).extract())
		fecha = get_date_nvzla(response.css(settings[self.name]['fecha']).extract())
		current_date = obtener_fecha_tipo10(fecha.split('T')[0])
		if(body!='' and current_date):
			yield {
			'titulo': response.css(settings[self.name]['titulo']).extract()[0],
			'autor': '',
			'fecha': fecha,
			'body': [body],
			'link': response.url,
			}
