import scrapy

from utils import *
from settings import settings

class SiteSpySpider(scrapy.Spider):
	
	name = "caraota_digital"
	start_urls = [settings[name]['url']]		
	
	def parse(self, response):
		for href in response.css(settings[self.name]['links']):
			full_url = response.urljoin(href.extract())
			yield scrapy.Request(full_url, callback=self.parse_links)	
						
	def parse_links(self, response):
		category = response.css('.entry-category a::text').extract()
		fecha = response.css(settings[self.name]['fecha']).extract()[0]
		current_date = obtener_fecha_tipo13(fecha)
		if(not(('Entretenimiento' in category) or ('Deportes' in category) or ('Curiosidades' in category) or ('author/' in response.url)) and current_date):
			body = limpiar(response.css(settings[self.name]['body']).extract())
			yield {
			'titulo': response.css(settings[self.name]['titulo']).extract()[0],
			'autor': response.css(settings[self.name]['autor']).extract()[0],
			'fecha': fecha,
			'body': [body],
			'link': response.url,
		}
