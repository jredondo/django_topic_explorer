from django.shortcuts import render
from django.views.generic import TemplateView
from django_topic_explorer.settings import FILES_PATH
from django.shortcuts import render, render_to_response
from django.template import RequestContext
import json,requests
from django_topic_explorer.settings import URL_COMUN
from django.utils.safestring import mark_safe

# Create your views here.

 
class verTopico(TemplateView):
    template_name='see_topic/topicos.html'
    
    def post(self, request, *args, **kwargs):
        buscar = request.POST['propuesta']
        num_topico = request.POST['topico']
        #obtener josn para utilizarlo en topicos.html
        r = requests.get(
          URL_COMUN+'topic_explorer/topics.json?format=json', 
        )
        #obtiene solo el apartado de palabras del json
        topicos = json.loads(r.content)
        mi_topico = {}
        mi_topico = self.obtenerValores(topicos,num_topico)
        print mi_topico
        mi_topico= json.dumps(mi_topico)
        #carga el pre-procesado del archivo en una variable
        texto=''
        direccion = FILES_PATH + '/'+ buscar
        try:
            archivo = open(direccion,'r')
            texto=archivo.read()
            archivo.close()
        except:
            buscar=''
        return render_to_response('see_topic/topicos.html',
                                  {'texto':texto,
                                   'topicos':mark_safe(mi_topico)},
                                  context_instance=RequestContext(request))
    
    
    def obtenerValores(self,topicos,num_topico):#funcion para obtener las palabras del json
        my_topic={}
        for x in topicos:
            if(x==num_topico):
                my_topic = topicos[x]['words']
                break
        return my_topic
        