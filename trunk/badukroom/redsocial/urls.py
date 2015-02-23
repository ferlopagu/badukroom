'''
Created on 21/01/2015

@author: fla2727
'''
from django.conf.urls import patterns, url
from redsocial.views import perfil, home, crea_comentario, buscador, agregar_ajax, contar_notificaciones, ver_notificaciones, aceptar_peticion, declinar_peticion, limpiar_notificaciones, eliminar_ajax, grupo, lista_grupos, responder, amigos, partidas, partidas_ajax
#from django.views.generic.base import TemplateView

#url(r'crea_comentario/$', crea_comentario.as_view(template_name="inicio"))
urlpatterns = patterns ('' ,
    url(r'^$', home, name='home'),
    url(r'^creaComentario/', crea_comentario, name='creaComentario'), #creaComentario coincide con la expresion regular inferior que al no encontrar username=creaComentario daba un error 404 por eso tenemos que poner antes la url de creaComentario
    url(r'^responder/', responder, name='responder'),
    url(r'^buscar/', buscador, name='buscar'),
    url(r'^agregar_ajax/', agregar_ajax, name='agregar_ajax'),
    url(r'^eliminar_ajax/', eliminar_ajax, name='eliminar_ajax'),
    url(r'^contar_notificaciones/', contar_notificaciones, name='contar_notificaciones'),
    url(r'^ver_notificaciones/', ver_notificaciones, name='ver_notificaciones'),
    url(r'^aceptar_peticion/', aceptar_peticion, name='aceptar_peticion'),
    url(r'^declinar_peticion/', declinar_peticion, name='declinar_peticion'),
    url(r'^limpiar_notificaciones/', limpiar_notificaciones, name='limpiar_notificaciones'),
    url(r'^mis_grupos/$', lista_grupos, name='lista_grupos'),
    url(r'^grupo/(?P<grupo_id>\d+)/$', grupo, name='grupo'),
    url(r'^amigos/', amigos, name='amigos'),
    url(r'^partidas/', partidas, name='partidas'),
    url(r'^partidas_ajax/', partidas_ajax, name="partidas_ajax"),
    url(r'^(?P<username>\w+)/$', perfil, name='perfil'),     
)