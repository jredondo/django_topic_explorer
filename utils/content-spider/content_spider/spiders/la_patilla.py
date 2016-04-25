import scrapy

from utils import *
from settings import settings

class SiteSpySpider(scrapy.Spider):
	
	name = "la_patilla"
	start_urls = [settings[name]['url']]		
	
	def parse(self, response):
		for href in response.css(settings[self.name]['links']):
			full_url = response.urljoin(href.extract())
			yield scrapy.Request(full_url, callback=self.parse_links)	
						
	def parse_links(self, response):
		category = response.css('.entry-cat a::text').extract()
		titulo = response.css(settings[self.name]['titulo']).extract()[0]
		fecha = response.css(settings[self.name]['fecha']).extract()[0]
		current_date = obtener_fecha_tipo3(fecha)
		if(not(('(Video)' in titulo) or ('(VIDEO)' in titulo) or ('(Fotos)' in titulo) or ('(foto)' in titulo) or ('Titulares' in category)) and current_date):
			yield {
			'titulo': titulo,
			'autor': response.css(settings[self.name]['autor']).extract()[0].replace('About ',''),
			'fecha': fecha,
			'body': response.css(settings[self.name]['body']).extract(),
			'link': response.url,
			}
