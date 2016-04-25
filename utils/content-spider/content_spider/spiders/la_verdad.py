import scrapy

from utils import *
from settings import settings

class SiteSpySpider(scrapy.Spider):
	
	name = "la_verdad"
	start_urls = [settings[name]['url']]		
	
	def parse(self, response):
		enlaces = get_glob_links(settings[self.name]['links'])
		for item in enlaces:
			yield scrapy.Request(item, callback=self.parse_links)
			
	def parse_links(self, response):
		fecha = response.css(settings[self.name]['fecha']).extract()[0]
		current_date = obtener_fecha_tipo9(fecha.split(" - ")[0])
		if(current_date):
			body = limpiar(response.css(settings[self.name]['body']).extract())
			yield {
			'titulo': response.css(settings[self.name]['titulo']).extract()[0],
			'autor': response.css(settings[self.name]['autor']).extract()[0],
			'fecha': fecha,
			'body': [body],
			'link': response.url,
			}
