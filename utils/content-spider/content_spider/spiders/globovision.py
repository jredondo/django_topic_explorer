import scrapy

from utils import *
from settings import settings

class SiteSpySpider(scrapy.Spider):
	
	name = "globovision"
	start_urls = [settings[name]['url']]		
	
	def parse(self, response):
		enlaces = get_glob_links(settings[self.name]['links'])
		for item in enlaces:
			yield scrapy.Request(item, callback=self.parse_links)
			
	def parse_links(self, response):
		fecha = response.css(settings[self.name]['fecha']).extract()[0]
		current_date = obtener_fecha_tipo6(fecha.split(" ")[1])
		if(current_date):
			body = limpiar(response.css(settings[self.name]['body']).extract())
			titulo = limpiar_fecha(response.css(settings[self.name]['titulo']).extract())
			autor = limpiar_fecha(response.css(settings[self.name]['autor']).extract())
			yield {
			'titulo': titulo,
			'autor': autor,
			'fecha': fecha,
			'body': [body],
			'link': response.url,
			}
