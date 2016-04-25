import scrapy

from utils import *
from settings import settings

class SiteSpySpider(scrapy.Spider):
	
	name = "quinto_dia"
	start_urls = [settings[name]['url']]		
	
	def parse(self, response):
		for href in response.css(settings[self.name]['links']):
			full_url = response.urljoin(href.extract())
			yield scrapy.Request(full_url, callback=self.parse_links)	
						
	def parse_links(self, response):
		body = limpiar_quintodia(response.css(settings[self.name]['body']).extract())
		yield {
		'titulo': response.css(settings[self.name]['titulo']).extract()[0],
		'autor': response.css(settings[self.name]['autor']).extract()[-1],
		'fecha': '',
		'body': [body],
		'link': response.url,
		}
