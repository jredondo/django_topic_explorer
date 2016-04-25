import scrapy

from utils import *
from settings import settings
import json

class SiteSpySpider(scrapy.Spider):
	
	name = "todochavez"
	start_urls = [settings[name]['url']]		
	
	def parse(self, response):
		js = json.loads(response.body)
		numero = 0
		for item in js['results']:
			if(item['numero']):
				numero = int(item['numero'])
			else:
				numero -=1
			full_url = 'http://www.todochavezenlaweb.gob.ve/todochavez/'+str(item['id'])+'-alo-presidente-n-'+str(numero)
			yield scrapy.Request(full_url, callback=self.parse_links)	
						
	def parse_links(self, response):
		yield {
		'titulo': response.css(settings[self.name]['titulo']).extract()[0],
		'fecha': response.css(settings[self.name]['fecha']).extract()[0],
		'body': response.css(settings[self.name]['body']).extract(),
		'link': response.url,
		}
