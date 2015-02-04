'''
Created on 21/01/2015

@author: fla2727
'''
from django.conf.urls import patterns, url
from redsocial.views import perfil, home, crea_comentario, buscador, agregar_ajax, contar_notificaciones
#from django.views.generic.base import TemplateView

#url(r'crea_comentario/$', crea_comentario.as_view(template_name="inicio"))
urlpatterns = patterns ('' ,
    url(r'^$', home, name='home'),
    url(r'^creaComentario/', crea_comentario, name='creaComentario'), #creaComentario coincide con la expresion regular inferior que al no encontrar username=creaComentario daba un error 404 por eso tenemos que poner antes la url de creaComentario
    url(r'^buscar/', buscador, name='buscar'),
    url(r'^agregar_ajax/', agregar_ajax, name='agregar_ajax'),
    url(r'^contar_notificaciones/', contar_notificaciones, name='contar_notificaciones'),
    url(r'^(?P<username>\w+)/$', perfil, name='perfil'),
    
    
)