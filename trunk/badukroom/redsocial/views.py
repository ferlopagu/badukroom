from django.shortcuts import render
from django.shortcuts import render_to_response
from django.core.context_processors import request
from django.contrib.auth.decorators import login_required
from django.template.context import RequestContext
from redsocial.models import Comentario
from login.models import Perfil

# Create your views here.
@login_required(login_url='/login')
def inicio(request):
    #return render_to_response('inicio.html', locals())
    
    """Este metodo devuelve los comentarios de un usuario, para mostrarlos en su dashboard
    recorremos todos los perfiles
    en un diccionario almacenamos {"perfil":perfilX}
    filtramos los comentarios por el perfil correspondiente
    Creamos una lista donde almacenaremos cada comentario
    add al diccionario que teniamos los comentarios de cada usuario dando como resultado un diccionario de la forma {"perfil":perfilX, "comentarios":[com1, com2]}
    add una lista con el diccionario de cada usuario siendo esta la que devolveremos
    """
    lista_diccionarios_def=[]
    perfiles=Perfil.objects.all()
    for p in perfiles:
        diccionario_perfil_comentarios={}
        diccionario_perfil_comentarios["perfil"]=p 
        comentarios=Comentario.objects.filter(perfil=p)
        lista_comentarios=[]
        for c in comentarios:
            lista_comentarios.append(c)
        diccionario_perfil_comentarios["comentarios"]=lista_comentarios
        lista_diccionarios_def.append(diccionario_perfil_comentarios)
        
    context = {'lista_diccionario_comentarios': lista_diccionarios_def}
    return render_to_response('inicio.html',context,context_instance=RequestContext(request))


""" Esto devuelve en la lista comentarios TODOS los comentarios del sistema
    lista_comentarios=[]
    perfiles=Perfil.objects.all()
    for p in perfiles:
        comentarios=Comentario.objects.filter(perfil=p)
        for c in comentarios:
            lista_comentarios.append(c)
    context = {'comentarios': lista_comentarios}
"""