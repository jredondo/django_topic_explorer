import scrapy

from utils import *
from settings import settings

class SiteSpySpider(scrapy.Spider):
	
	name = "noticias24"
	start_urls = [settings[name]['url']]		
	
	def parse(self, response):
		for href in response.css(settings[self.name]['links']):
			full_url = response.urljoin(href.extract())
			yield scrapy.Request(full_url, callback=self.parse_links)	
						
	def parse_links(self, response):
		if(not('fotos/' in response.url)):
		fecha = limpiar_fecha_n24([response.css(settings[self.name]['fecha'][0]).extract(),response.css(settings[self.name]['fecha'][1]).extract()])
		current_date = obtener_fecha_tipo5(fecha)
		if(current_date):
			body = limpiar_not24(response.css(settings[self.name]['body']).extract())
			yield {
			'titulo': response.css(settings[self.name]['titulo']).extract()[0],
			'autor': '',
			'fecha': fecha,
			'body': [body],
			'link': response.url,
			}
