# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.template.context import RequestContext
from redsocial.models import Comentario, Respuesta, PeticionAmistad
from login.models import Perfil
from django.shortcuts import get_object_or_404
from django.db.models import Q
from redsocial.forms import ComentarioForm
from django.http import JsonResponse
from datetime import datetime
from django.http.response import HttpResponseRedirect
from django.http import HttpResponse
from django.contrib.auth.models import User
import re
# Create your views here.
#@login_required(login_url='/login')
def perfil(request, username):
    print request.user
    #return render_to_response('inicio.html', locals())   
    """Probamos version pasandole directamente el username
    1º Capturamos username de la url
    2º Buscamos el perfil con el que coincide
    3º Recogemos lista de diccionarios def que contendra diccionarios (diccionario_perfil_comentarios)
    4º Estos diccionarios seran {"perfil":p, "comentarios"=lista de diccionarios con comentarios y sus respuestas (diccionario_comentarios_respuestas)  }
    5º diccionario_comentarios_respuestas ---> {"comentario":c, "respuestas"=[r1,r2,r3,...]}
    6º devolvemos lista_diccionarios_def, que sera de la forma:  [{"perfil":fla2727,"comentarios": [{"comentario":c, "respuestas":[r1,r2]},..]}, y asi para cada perfil ]
    7º recogemos las imagenes de perfil y portada del perfil
    8º creamos el formulario para comentar
    9º Comprobar si el usuario que vemos es amigo nuestro, 
    en caso negativo devolver variable para imprimir en el template un boton de agregar como amigo
    en caso afirmativo devolver variable para imprimir en el template un boton de eliminar
    """
    #Pasos 1 a 6
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
    
    
    #Paso 7
    """
    Almacenar un string con el path de la imagen principal el cual no estamos almacenando en la base de datos como si hacemos en el modelo Partida
    """
    path_perfil=p.foto_principal.name.__str__()
    m1 = re.match(".*/(imagenes/.*)", path_perfil)
    print path_perfil
    print m1.group(1)
    perfil= m1.group(1)
    
    path_portada=p.foto_portada.name.__str__() #es posible hacerlo asi supuestamente p.foto_portada.url
    m2 = re.match(".*/(imagenes/.*)", path_portada)
    portada=m2.group(1)
    
    dic_imagenes={'perfil':perfil,'portada':portada}
    print dic_imagenes
    lista_dic_imagenes=[]
    lista_dic_imagenes.append(dic_imagenes)
    """fin almacenar"""
    
    #Paso 8
    """ add form comentar"""
    formulario=ComentarioForm()
    
    
    #Paso 9
    """comprobamos si el perfil que visualizamos somos nosotros, es un amigo o desconocido """
    somos_nosotros=False
    es_amigo=False
    
    if username == request.user.username:
        """ el perfil que vemos es el nuestro"""
        somos_nosotros=True
        print "somos nosotros"
    else:
        """comprobamos si es amigo"""
        for amigo in p.amigos.all(): 
            print "amigo:"+amigo.__unicode__()
            if amigo.user.username == request.user.username:
                print username+"es amigo de"+amigo.user.username
                es_amigo=True
            else:
                print "no son amigos"
    diccionario_amigos={"somos_nosotros":somos_nosotros,"es_amigo":es_amigo}
    print diccionario_amigos
    lista_dic_amigo=[]
    lista_dic_amigo.append(diccionario_amigos) #devolvemos lista con diccionario unico donde especifica si es amigo o no el perfil que visitamos
    
    
    context = {'lista_diccionario_comentarios': lista_diccionarios_def, 'formulario':formulario, 'lista_dic_imagenes':lista_dic_imagenes, 'lista_dic_amigo':lista_dic_amigo}
    return render_to_response('perfil.html',context,context_instance=RequestContext(request))

@login_required(login_url='/login')
def home(request):
    #REvisar el bucle porque cuando no tiene amigos no muestra ni sus propios comentarios
    username=request.user.username
    lista_comentarios=[]
    p = get_object_or_404(Perfil, user__username=username)
    for amigo in p.amigos.all():
        comentarios=Comentario.objects.filter(Q(perfil=amigo)|Q(perfil=p)).order_by('fecha').reverse()
        for c in comentarios:
            lista_comentarios.append(c)
    print lista_comentarios
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
        return HttpResponseRedirect(request.META['HTTP_REFERER'])
        #home(request)
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

def agregar_ajax(request):
    #revisar falta de else para todos los if
    if request.is_ajax():
        if request.method=='POST':
            print "Esto contiene request.Post['perfil_para_agregar]: "+request.POST['perfil_para_agregar']
            username_receptor=request.POST['perfil_para_agregar']
            emisor=get_object_or_404(Perfil, user__username=request.user.username)
            receptor=get_object_or_404(Perfil, user__username=username_receptor)
            es_aceptada=False
            es_rechazada=False
            print emisor
            print receptor
            peticion=PeticionAmistad(emisor=emisor, receptor=receptor, es_aceptada=es_aceptada, es_rechazada=es_rechazada)
            peticion.save()
            return HttpResponse("Peticion de amistad enviada con éxito")
    else:
        print "fue un fracaso la peticion ajax"

def contar_notificaciones(request):
    if request.is_ajax():
        if request.method=='GET':
            recuento = PeticionAmistad.objects.filter(receptor__user__username=request.user.username).count()
            print "Recuento: "+recuento.__str__()
            return HttpResponse(recuento)
    else:
        print "no es peticion ajax o GET"
        return HttpResponse("no es peticion ajax o GET")
        
           
