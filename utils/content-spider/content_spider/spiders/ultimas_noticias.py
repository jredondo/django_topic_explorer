import scrapy
from scrapy.http import HtmlResponse

from utils import *
from settings import settings

class SiteSpySpider(scrapy.Spider):
	
	name = "ultimas_noticias"
	start_urls = [settings[name]['url']]		
	
	def parse(self, response):
		for href in response.css(settings[self.name]['links']):
			full_url = response.urljoin(href.extract())
			yield scrapy.Request(full_url, callback=self.parse_links)	
						
	def parse_links(self, response):
		try:
			reponse.css
		except:
			response = HtmlResponse(url=response.url,body=response.body)
		fecha = limpiar_autor_tc(response.css(settings[self.name]['fecha']).extract()[0].split('|')[1])
		current_date = True
		if(len(fecha)>10):
			current_date = obtener_fecha_tipo6(fecha.split(" ")[0])
		if(current_date):
			titulo = limpiar_autor_tc(response.css(settings[self.name]['titulo']).extract()[0])
			body = limpiar_ult_n(response.css(settings[self.name]['body']).extract())
			yield {
			'titulo': titulo,
			'autor': response.css(settings[self.name]['autor']).extract()[0],
			'fecha': fecha,
			'body': [body],
			'link': response.url,
			}
