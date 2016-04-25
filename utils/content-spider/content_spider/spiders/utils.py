import feedparser
from BeautifulSoup import BeautifulSoup
from datetime import date

#Funciones para limpiar los cuerpos de los diarios
def limpiar(var,init=0):
	cont_str = ''
	for i in range(init,len(var)):
		clean = BeautifulSoup(var[i]).text
		if(clean!=''):
			cont_str += clean
			cont_str += '\n'
	return cont_str
	
def limpiar_dt(var):
	var = limpiar(var,1)
	return var
	
def limpiar_eu(var):
	cont_str = ''
	for item in var:
		cen = limpiar(item)
		if(len(cen)>10):
			cont_str += cen
	cont_str = cont_str.replace('Contenido relacionado','')
	return cont_str
	
def limpiar_un(var):
	return var.replace('\t','').replace('\r','').replace('\n','')
	
	
def limpiar_vene(var):
	var = var[0]
	fin = var.find("</span>")+len("</span>")
	var = var[fin:]
	cont_str = BeautifulSoup(var).text
	return cont_str
	
def limpiar_notdigital(var):
	body = limpiar(var,1)
	body = body.replace('\nvaya al foro\n',' ')
	inicio = body.find('\nEtiquetas')
	body = body[:inicio]
	inicio = body.find('.-')
	body = body[inicio+len('.-'):]
	return body
	
def limpiar_quintodia(var):
	number = 0
	for i in range(0,len(var)):
		if('<strong>' in var[(len(var)-1)-i]):
			number = (len(var)-1)-i
			break
	cont_str = ''
	for i in range(0,number):
		clean = BeautifulSoup(var[i]).text
		if(clean!=''):
			cont_str += clean
			cont_str += '\n'
	return cont_str
	
def limpiar_ult_n(var):
	cont_str = ''
	for i in range(0,len(var)):
		if('twitter' in var[i]):
			break
		clean = BeautifulSoup(var[i]).text
		if(not('@' in clean)):
			cont_str += clean
			cont_str += '\n'
	inicio = cont_str.find('<br  />')
	cont_str = cont_str[:inicio]
	inicio = cont_str.find('.-')
	cont_str = cont_str[inicio+len('.-'):].strip()
	return cont_str
	
def limpiar_not_vzla(var):
	cont_str = ''
	for i in range(0,len(var)):
		if(var[i].find('<iframe')):
			inicio = var[i].find('<iframe')
			var[i] = var[i][:inicio]
		clean = BeautifulSoup(var[i]).text
		if(clean!=''):
			cont_str += clean
			cont_str += '\n'
	inicio = cont_str.find('Noticias Abajo')
	cont_str = cont_str[:inicio]
	inicio = cont_str.find('[email')
	cont_str = cont_str[:inicio]
	inicio = cont_str.find('pic.twitter')
	cont_str = cont_str[:inicio]
	inicio = cont_str.find('NO OLVIDES DEJAR ')
	cont_str = cont_str[:inicio]
	inicio = cont_str.find('Fuente:')
	cont_str = cont_str[:inicio]
	inicio = cont_str.find('(adsbygoogle')
	cont_str = cont_str[:inicio]
	return cont_str
	
def limpiar_not24(var):
	var = limpiar(var)
	inicio = var.find('.-')
	var = var[inicio+len('.-'):]
	return var
	
#Funciones para limpiar las fechas	
def limpiar_fecha(var):
	for item in var:
		date = BeautifulSoup(item).text
		if(date!=''):
			fecha = date
	return fecha
	
def limpiar_fecha_n24(var):
	date = ''
	for item in var:
		if(item):
			date += limpiar_fecha(item)
	return date
	
def limpiar_fecha_ub(var):
	var = BeautifulSoup(var).text
	inicio = var.find('-')
	var = var[:inicio]
	return var
	
#Funcion para limpiar el campo autor
def limpiar_autor_tc(var):
	return var.replace('\r','').replace('\n','').replace('\t','').strip()

#Funciones para revisar rss
def get_all_links(links):
	feeds = []
	enlaces = []
	for item in links:
		feeds.append(feedparser.parse(links[item]))
	for item in feeds:
		for value in item['entries']:
			if value['link'] not in enlaces:
				enlaces.append(value['link'])
	return enlaces
	
def get_glob_links(var):
	feed = feedparser.parse(var)
	enlaces = []
	for item in feed['entries']:
		enlaces.append(item['link'])
	return enlaces

#Funciones para obtener datos ocultos(fechas, autores,etc)
def get_date_nvzla(var):
	const_str = ''
	for item in var:
		if 'article:published_time' in item:
			inicio = item.find('content')
			my_str = item[inicio:]
			inicio = my_str.find("\"")
			my_str = my_str[inicio+1:-2]
			return my_str
			
def get_author_eu(var):
	
	for item in var:
		if 'author' in item:
			inicio = item.find('content')
			my_str = item[inicio:]
			inicio = my_str.find("\"")
			my_str = my_str[inicio+1:-2]
			return my_str

#Funcion para generar una str de una lista de listas
def get_body_en(var):
	const_str = '' 
	for item in var:
		for x in item:
			if(x):
				const_str += x + "\n"				
	return const_str
	

#Funciones para generar fechas en python
def get_es_date(var):
	if(var=='01'):
		return 'enero'
	elif(var=='02'):
		return 'febrero'
	elif(var=='03'):
		return 'marzo'
	elif(var=='04'):
		return 'abril'
	elif(var=='05'):
		return 'mayo'
	elif(var=='06'):
		return 'junio'
	elif(var=='07'):
		return 'julio'
	elif(var=='08'):
		return 'agosto'
	elif(var=='09'):
		return 'septiembre'
	elif(var=='10'):
		return 'octubre'
	elif(var=='11'):
		return 'noviembre'
	elif(var=='12'):
		return 'diciembre'
		
def get_res_date(var):
	if(var=='01'):
		return 'ene'
	elif(var=='02'):
		return 'feb'
	elif(var=='03'):
		return 'mar'
	elif(var=='04'):
		return 'abr'
	elif(var=='05'):
		return 'may'
	elif(var=='06'):
		return 'jun'
	elif(var=='07'):
		return 'jul'
	elif(var=='08'):
		return 'ago'
	elif(var=='09'):
		return 'sep'
	elif(var=='10'):
		return 'oct'
	elif(var=='11'):
		return 'nov'
	elif(var=='12'):
		return 'dic'
		
#fecha tipo: 04 de abril 2016		
def obtener_fecha_tipo1(var):
	var = var.split("-")[0]
	b = var.strip().split(" ")
	if(len(b[0])<2):
		b[0] = "0"+b[0]
		var = " ".join(b)
	d = date.today()
	mes = get_es_date(d.strftime('%m'))
	fecha = str(d.strftime('%d de ')+mes+d.strftime(' %Y'))
	if(var==fecha):
		return True
	else:
		return False
		
#fecha tipo: 04 de abril de 2016		
def obtener_fecha_tipo2(var):
	b = var.split(" ")[:-2]
	var = " ".join(b)
	return obtener_fecha_orig1(var)
		
def obtener_fecha_orig1(var):
	d = date.today()
	mes = get_es_date(d.strftime('%m'))
	fecha = str(d.strftime('%d de ')+mes+d.strftime(' de %Y'))
	if(var==fecha):
		return True
	else:
		return False
		
#fecha tipo: abril 4, 2016		
def obtener_fecha_tipo3(var):
	b = var.split(" ")[:-2]
	if(len(b[1])<3):
		b[1] = "0"+b[1]
	var = " ".join(b)
	d = date.today()
	mes = get_es_date(d.strftime('%m'))
	fecha = str(mes+d.strftime(' %d, %Y'))
	if(var==fecha):
		return True
	else:
		return False
		
#fecha tipo: apr 4, 2016		
def obtener_fecha_tipo4(var):
	b = var.split(" ")[1:-3]
	if(len(b[1])<3):
		b[1] = "0"+b[1]
	var = " ".join(b)
	d = date.today()
	fecha = str(d.strftime('%b %d, %Y'))
	if(var==fecha):
		return True
	else:
		return False
		
#fecha tipo: 04 de abr de 2016		
def obtener_fecha_tipo5(var):
	b = var.split(" ")[:-2]
	var = " ".join(b)
	d = date.today()
	mes = get_res_date(d.strftime('%m'))
	fecha = str(d.strftime('%d de ')+mes+d.strftime(' de %Y'))
	if(var==fecha):
		return True
	else:
		return False
		
#fecha tipo: 04-04-2016		
def obtener_fecha_tipo6(var):
	d = date.today()
	fecha = str(d.strftime('%d-%m-%Y'))
	if(var==fecha):
		return True
	else:
		return False

#fecha tipo: 04/04/2016		
def obtener_fecha_tipo7(var):
	b = var.split(" ")[1:-2]
	var = " ".join(b)
	return obtener_fecha_orig2(var)
	
def obtener_fecha_orig2(var):
	d = date.today()
	fecha = str(d.strftime('%d/%m/%Y'))
	if(var==fecha):
		return True
	else:
		return False
		
#fecha tipo: 4 Abril, 2016	
def obtener_fecha_tipo8(var):
	b = var.split(" ")
	if(len(b[0])<2):
		b[0] = "0"+b[0]
	var = " ".join(b)
	d = date.today()
	mes = get_es_date(d.strftime('%m')).capitalize()+","
	fecha = str(d.strftime('%d ')+mes+d.strftime(' %Y'))
	print var
	print fecha
	if(var==fecha):
		return True
	else:
		return False
		
#fecha tipo: 04 de Abril de 2016		
def obtener_fecha_tipo9(var):
	d = date.today()
	mes = get_es_date(d.strftime('%m')).capitalize()
	fecha = str(d.strftime('%d de ')+mes+d.strftime(' de %Y'))
	if(var==fecha):
		return True
	else:
		return False


#fecha tipo: 2016-04-05(Y-m-d)		
def obtener_fecha_tipo10(var):
	d = date.today()
	fecha = str(d.strftime('%Y-%m-%d'))
	if(var==fecha):
		return True
	else:
		return False
		
#fecha tipo: 04 de Abril de 2016		
def obtener_fecha_tipo11(var):
	b = var.split(" ")[1:-3]
	var = " ".join(b)
	return obtener_fecha_tipo9(var)
	
#fecha tipo: 04 de abril de 2016		
def obtener_fecha_tipo12(var):
	b = var.split(" ")
	if(len(b[0])<2):
		b[0] = "0"+b[0]
	var = " ".join(b)
	return obtener_fecha_orig1(var)

#fecha tipo: abr 4, 2016		
def obtener_fecha_tipo13(var):
	b = var.split(" ")
	if(len(b[1])<3):
		b[1] = "0"+b[1]
	var = " ".join(b)
	d = date.today()
	mes = get_res_date(d.strftime('%m'))
	fecha = str(mes+d.strftime(' %d, %Y'))
	if(var==fecha):
		return True
	else:
		return False
