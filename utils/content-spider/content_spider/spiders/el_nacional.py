import scrapy

from utils import *
from settings import settings

class SiteSpySpider(scrapy.Spider):
	
	name = "el_nacional"
	start_urls = [settings[name]['url']]		
	
	def parse(self, response):
		for href in response.css(settings[self.name]['links']):
			full_url = response.urljoin(href.extract())
			yield scrapy.Request(full_url, callback=self.parse_links)
				
	def parse_links(self, response):
		fecha = response.css(settings[self.name]['fecha']).extract()[0]
		current_date = obtener_fecha_tipo1(fecha)
		if(current_date):
			body = get_body_en([response.css(settings[self.name]['body'][0]).extract(),response.css(settings[self.name]['body'][1]).extract()])
			yield {
			'titulo': response.css(settings[self.name]['titulo']).extract()[0],
			'autor': response.css(settings[self.name]['autor']).extract()[0],
			'fecha': fecha,
			'body': [body],
			'link': response.url,
			}
