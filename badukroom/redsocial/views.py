from django.shortcuts import render
from django.shortcuts import render_to_response
from django.core.context_processors import request
from django.contrib.auth.decorators import login_required
from django.template.context import RequestContext
from redsocial.models import Comentario, Respuesta
from login.models import Perfil
from django.shortcuts import get_object_or_404
from django.db.models import Q
from django.views.generic.base import TemplateView
from redsocial.forms import ComentarioForm
from django.http import JsonResponse
from datetime import datetime
from django.http.response import HttpResponseRedirect
from Tkconstants import CHAR
from django.conf.urls import url
from django.contrib.auth.models import User

# Create your views here.
#@login_required(login_url='/login')
def inicio(request, username):
    #return render_to_response('inicio.html', locals())
    
    """Este metodo devuelve los comentarios de un usuario, para mostrarlos en su dashboard
    recorremos todos los perfiles
    en un diccionario almacenamos {"perfil":perfilX}
    filtramos los comentarios por el perfil correspondiente
    Creamos una lista donde almacenaremos cada comentario
    add al diccionario que teniamos los comentarios de cada usuario dando como resultado un diccionario de la forma {"perfil":perfilX, "comentarios":[com1, com2]}
    add una lista con el diccionario de cada usuario siendo esta la que devolveremos
    """
    """ VERSION ANTIGUA FUNCIONAL
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
    """
    
    """ PROBAMOS VERSION NUEVA PARA ADD LAS RESPUESTAS """
    """
    lista_diccionarios_def=[]
    perfiles=Perfil.objects.all()
    for p in perfiles:
        diccionario_perfil_comentarios={}
        diccionario_perfil_comentarios["perfil"]=p 
        comentarios=Comentario.objects.filter(perfil=p)
        lista_diccionario_comentarios_respuestas=[] #va a almacenar una lista del diccionario siguiente
        for c in comentarios:
            diccionario_comentarios_respuestas={}# diccionario = {'comentario': r1, 'respuestas': [r1,r2,r3]}
            diccionario_comentarios_respuestas['comentario']=c
            resp=Respuesta.objects.filter(comentario=c)
            respuestas=[]
            for r in resp:
                respuestas.append(r)
            diccionario_comentarios_respuestas['respuestas']=respuestas
            lista_diccionario_comentarios_respuestas.append(diccionario_comentarios_respuestas)
        diccionario_perfil_comentarios['comentarios']=lista_diccionario_comentarios_respuestas
        lista_diccionarios_def.append(diccionario_perfil_comentarios)
    context = {'lista_diccionario_comentarios': lista_diccionarios_def}
    return render_to_response('inicio.html',context,context_instance=RequestContext(request))

    """
    
    """Probamos version pasandole directamente el username"""
    lista_diccionarios_def=[]
    p = get_object_or_404(Perfil, user__username=username)
    diccionario_perfil_comentarios={}
    diccionario_perfil_comentarios["perfil"]=p 
    comentarios=Comentario.objects.filter(perfil=p)
    lista_diccionario_comentarios_respuestas=[] #va a almacenar una lista del diccionario siguiente
    for c in comentarios:
        diccionario_comentarios_respuestas={}# diccionario = {'comentario': r1, 'respuestas': [r1,r2,r3]}
        diccionario_comentarios_respuestas['comentario']=c
        resp=Respuesta.objects.filter(comentario=c)
        respuestas=[]
        for r in resp:
            respuestas.append(r)
        diccionario_comentarios_respuestas['respuestas']=respuestas
        lista_diccionario_comentarios_respuestas.append(diccionario_comentarios_respuestas)
    diccionario_perfil_comentarios['comentarios']=lista_diccionario_comentarios_respuestas
    lista_diccionarios_def.append(diccionario_perfil_comentarios)
    """ add form comentar"""
    formulario=ComentarioForm()
    context = {'lista_diccionario_comentarios': lista_diccionarios_def, 'formulario':formulario}
    return render_to_response('inicio.html',context,context_instance=RequestContext(request))

@login_required(login_url='/login')
def home(request):
    username=request.user.username
    lista_comentarios=[]
    p = get_object_or_404(Perfil, user__username=username)
    for amigo in p.amigos.all():
        comentarios=Comentario.objects.filter(Q(perfil=amigo)|Q(perfil=p)).order_by('fecha').reverse()
        for c in comentarios:
            lista_comentarios.append(c)
    context = {'lista_comentarios': lista_comentarios}
    return render_to_response('home.html',context,context_instance=RequestContext(request))


    
def crea_comentario(request):
    if request.is_ajax():
        #formulario=ComentarioForm(texto=request.POST['texto'])
        form = ComentarioForm(request.POST)
        if form.is_valid():
            #form.save()
            comentario=form.save(commit=False)
            comentario.fecha=datetime.now()
            perfil=Perfil.objects.get(user=request.user)
            comentario.perfil=perfil
            comentario.save()
            comentarios=list(Comentario.objects.values())
            return JsonResponse(comentarios, safe=False)
    else:
        print "ENTRAMOS EN ELSE AL NO SER AJAX"
        home(request)
        #print "JEJEJEJEJEJEJEJEJEJEJEJEJEJJEJ"
        #formulario=ComentarioForm()
        #comentarios=list(Comentario.objects.values())
        #print comentarios
        #context = {'formulario':formulario, 'comentarios':comentarios}
        #return render_to_response('comentar.html',context,context_instance=RequestContext(request))

def buscador(request):
    if request.is_ajax():
        if request.method=='POST':
            print "Esto contiene request.POST: "+request.POST['texto']
            cadena=request.POST['texto']
            lista_perfiles=list(Perfil.objects.values('user').filter(Q(user__first_name__iregex=cadena) | Q(user__last_name__iregex=cadena))) #cambiar username por first_name o last_name
            print lista_perfiles
            for p in lista_perfiles:
                lista_user=list(User.objects.values('first_name', 'last_name', 'username').filter(id=p['user']))
            
            print lista_user
            return JsonResponse(lista_user, safe=False)
            """
            print lista_perfiles
            context={'lista_perfiles',lista_perfiles}
            return render_to_response('busqueda.html', context, context_instance=RequestContext(request))
            """
        else:
            render("Hubo un problema en su peticion")
    else:
        
        return HttpResponseRedirect(request.META['HTTP_REFERER'])
