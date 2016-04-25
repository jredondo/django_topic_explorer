import scrapy

from utils import *
from settings import settings

links_venevision = {"Nacionales":"http://feeds.feedburner.com/CanalNacionales","Politica":"http://feeds.feedburner.com/CanalPoltica",
"Internacionales":"http://feeds.feedburner.com/CanalInternacionales","Economia":"http://feeds.feedburner.com/CanalEconomia"}

class SiteSpySpider(scrapy.Spider):
	
	name = "venevision"
	start_urls = [settings[name]['url']]		
	
	def parse(self, response):
		enlaces = get_all_links(links_venevision)
		for item in enlaces:
			yield scrapy.Request(item, callback=self.parse_links)
			
	def parse_links(self, response):
		fecha = limpiar_fecha(response.css(settings[self.name]['fecha']).extract())
		current_date = obtener_fecha_tipo7(fecha)
		if(current_date):
			body = limpiar_vene(response.css(settings[self.name]['body']).extract())
			yield {
			'titulo': response.css(settings[self.name]['titulo']).extract()[0],
			'autor': '',
			'fecha': fecha,
			'body': [body],
			'link': response.url,
			}
