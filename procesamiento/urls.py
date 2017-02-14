# -*- coding: utf-8 -*-
"""
Sistema de Modelado de Tópicos

Copyleft (@) 2014 CENDITEL nodo Mérida - https://planificacion.cenditel.gob.ve/trac/
"""
## @package django_topic_explorer.procesamiento.urls
#
# Urls de la aplicación de procesamiento
# @author Rodrigo Boet (rboet at cenditel.gob.ve)
# @author <a href='http://www.cenditel.gob.ve'>Centro Nacional de Desarrollo e Investigación en Tecnologías Libres
# (CENDITEL) nodo Mérida - Venezuela</a>
# @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
# @version 1.3
from django.conf.urls import include, url

from .views import *


urlpatterns = [
    url(r'^$', ProcesamientoCreate.as_view(), name='procesamiento_index'),
]