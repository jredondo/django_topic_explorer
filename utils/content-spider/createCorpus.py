import sys
import os
import json

def individual(filename,directorio):
	js = json.loads(open(filename,'r').read())
	i = 0
	for item in js:
		cuerpo = ''
		for body in item['body']:
			cuerpo += body.encode('utf-8-sig')+" "
		if(os.path.exists(directorio+"/propesta_"+str(i))):
			i = len(os.listdir('corpus'))
		archivo = open(directorio+"/propesta_"+str(i),'w')
		#archivo = open(directorio+"/"+item['titulo'],'w')
		archivo.write(item['titulo'].encode('utf-8-sig'))
		archivo.write("\n\n")
		archivo.write(cuerpo)
		archivo.close()
		i+=1
				
if __name__ == '__main__':
	directorio = 'corpus'
	if(len(sys.argv)>1):
		filename = sys.argv[1]
		if(len(sys.argv)>2):
			directorio = sys.argv[2]
		if not os.path.exists(directorio):
			os.makedirs(directorio)
		if(filename!='all'):
			individual(filename,directorio)
		else:
			x = [x for x in os.listdir(".") if(".json" in x)]
			for item in x:
				individual(item,directorio)
	else:
		print "Debe ingresar el nombre del json"
