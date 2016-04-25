import scrapy

from utils import *
from settings import settings

class SiteSpySpider(scrapy.Spider):
	
	name = "dolar_today"
	start_urls = [settings[name]['url']]		
	
	def parse(self, response):
		for href in response.css(settings[self.name]['links']):
			full_url = response.urljoin(href.extract())
			yield scrapy.Request(full_url, callback=self.parse_links)	
						
	def parse_links(self, response):
		fecha = response.css(settings[self.name]['autor']).extract()[0].split('/')[1].replace('@','')
		current_date = obtener_fecha_tipo4(fecha)
		titulo = response.css(settings[self.name]['titulo']).extract_first()
		if(not(('[IMAGEN]' in titulo) or ('[VIDEO]' in titulo) or ('[FOTO]' in titulo) or ('[FOTOS]' in titulo) or ('[DOCUMENTAL]' in titulo)) and current_date):
			body = limpiar_dt(response.css(settings[self.name]['body']).extract())
			yield {
			'titulo': titulo,
			'autor': response.css(settings[self.name]['autor']).extract()[0].split('/')[0].replace('@',''),
			'fecha': fecha,
			'body': [body],
			'link': response.url,
			}
