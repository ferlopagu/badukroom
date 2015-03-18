# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.template.context import RequestContext
from redsocial.models import Comentario, Respuesta, PeticionAmistad, Notificacion, Grupo, PeticionRevision
from login.models import Perfil
from django.shortcuts import get_object_or_404
from django.db.models import Q
from redsocial.forms import ComentarioForm, GrupoForm, EnvioForm, SgfForm, FechasForm
from django.http import JsonResponse
from datetime import datetime
from django.http.response import HttpResponseRedirect
from django.contrib.auth.models import User
import re
from principal.metodosAux import informacion_partida, informacion_partida2, estamos_en_grupo, formatoFecha
from badukroom.settings import BASE_DIR
from principal.models import Partida, Jugador, Revisor, PartidaRepositorio
from django.http import HttpResponse, HttpResponseBadRequest
from django.core.paginator import Paginator, InvalidPage
import json
from django.core import serializers
from django.template.defaultfilters import safe
from django.views.generic.base import TemplateView
from .recomendacion import perfiles_amigos, topMatches_amigos_comun, topMatches_gustos, getRecommendations_jugadores
from redsocial.recomendacion import perfiles_gustos
# Create your views here.
#return render_to_response('inicio.html', locals())   

def perfil(request, username):
    #p = get_object_or_404(Perfil, user__username=username) 
    #comentarios=list(Comentario.objects.filter(perfil=p, grupo=None).order_by('fecha').reverse())
    
    p = get_object_or_404(Perfil, user__username=username) 
    comentarios_list=list(Comentario.objects.filter(perfil=p, grupo=None).order_by('fecha').reverse())
    paginator=Paginator(comentarios_list,5)
    comentarios=paginator.page(1).object_list
    
    """comprobamos si el perfil que visualizamos somos nosotros, es un amigo o desconocido """
    somos_nosotros=False
    es_amigo=False
    peticion_enviada=False
    peticion_recibida=False
    if username == request.user.username:
        """ el perfil que vemos es el nuestro"""
        somos_nosotros=True
    else:
        """comprobamos si es amigo"""
        for amigo in p.amigos.all(): 
            if amigo.user.username == request.user.username:
                print request.user.username+" es amigo de "+amigo.user.username
                es_amigo=True
        if es_amigo==False:
            """ si no es amigo tres casos:
                    - Le hemos mandado una peticion de amistad, luego deberiamos ver 'La peticion fue enviada'
                    - Hemos recibido una peticion suya, luego debemos ver 'Aceptar peticion' y 'Rechazar peticion'
                    - No hay peticiones entre ambos, no somos amigos, luego debemos ver 'Agregar como amigo'
            """
            usuario_logueado= get_object_or_404(Perfil, user__username=request.user.username) 
            if PeticionAmistad.objects.filter(emisor=usuario_logueado, receptor=p):
                peticion_enviada=True
                print 'Existe peticion de '+usuario_logueado.user.username+' a '+p.user.username
            elif PeticionAmistad.objects.filter(emisor=p, receptor=usuario_logueado):
                peticion_recibida=True
                print 'Existe peticion de '+p.user.username+' a '+usuario_logueado.user.username
            else:
                print 'ni son amigos ni le envio la peticion'
    """ FIN comprobamos si el perfil que visualizamos somos nosotros, es un amigo o desconocido """                       
    diccionario_amigos={"somos_nosotros":somos_nosotros,"es_amigo":es_amigo, 'peticion_enviada':peticion_enviada, 'peticion_recibida':peticion_recibida}
    lista_dic_amigo=[]
    lista_dic_amigo.append(diccionario_amigos) #devolvemos lista con diccionario unico donde especifica si es amigo o no el perfil que visitamos
    
    amigos=p.amigos.all()
    grupos=list(Grupo.objects.filter(miembros__user__username=p.user.username))
    
    formulario_respuesta=ComentarioForm() #formulario para responder a los comentarios
    context = {'comentarios': comentarios, 'formulario_respuesta':formulario_respuesta,'lista_dic_amigo':lista_dic_amigo, 'perfil':p, 'amigos':amigos, 'grupos':grupos}
    
    if somos_nosotros==True: #somos nosotros luego add formulario para actualizar estado
        formulario=ComentarioForm()
        context['formulario']=formulario
    return render_to_response('perfil.html',context,context_instance=RequestContext(request))

def perfil_ajax(request, username):
    p = get_object_or_404(Perfil, user__username=username) 
    comentarios_list=list(Comentario.objects.filter(perfil=p, grupo=None).order_by('fecha').reverse())
    paginator=Paginator(comentarios_list,5)
    print("Entramos en perfil ajax")
    if request.is_ajax():
        if request.method=="GET":
            if request.GET.get("page_number"):
                print "entramos en get"
                page_number=request.GET.get('page_number')
                print page_number
                try:
                    comentarios=paginator.page(page_number).object_list
                except InvalidPage:
                    #return HttpResponseBadRequest(mimetype='json')
                    comentarios=[]
                lista_comentarios=[]
                for c in comentarios:
                    dic_comentario={}
                    dic_comentario["id"]=c.id
                    dic_comentario["nombre"]=c.perfil.user.first_name
                    dic_comentario["username"]=c.perfil.user.username
                    dic_comentario["path_principal"]=c.perfil.path_principal
                    dic_comentario["grupo"]=c.grupo
                    dic_comentario["fecha"]=c.fecha
                    dic_comentario["texto"]=c.texto
                    if c.partida != None:
                        dic_comentario["partida"]=c.partida.path
                    else:
                        dic_comentario["partida"]=""
                    resp=Respuesta.objects.filter(comentario=c)
                    lista_respuestas=[]
                    for r in resp:
                        dic_respuesta={"texto":r.texto,"fecha":r.fecha, "imagen_perfil":r.perfil.path_principal}
                        if r.partida != None:
                            dic_respuesta["partida"]=r.partida.path
                        else:
                            dic_respuesta["partida"]=""
                        lista_respuestas.append(dic_respuesta)
                    dic_comentario["respuestas"]=lista_respuestas
                    lista_comentarios.append(dic_comentario)
                print JsonResponse(lista_comentarios, safe=False)
                return JsonResponse(lista_comentarios, safe=False)


#@login_required(login_url='/login')
def perfil2(request, username):
    print request.user
 
    """
    Con esta vista vamos a visualizar los perfiles de los usuarios, tanto el del usuario que se loguea como el de los demas.
    Probamos version pasandole directamente el username
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
    comentarios=Comentario.objects.filter(perfil=p).order_by('fecha').reverse()
    #comentarios=Comentario.objects.values().filter(perfil=p).order_by('fecha').reverse()
    print comentarios
    lista_diccionario_comentarios_respuestas=[] #va a almacenar una lista del diccionario siguiente
    for c in comentarios:
        if c.grupo == None:
            print "Es nulo"
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
    print lista_diccionarios_def
    
    #Paso 7 devolver imagenes de portada y perfil
    perfil=p.path_principal
    print "Contenido p.path_principal: "+perfil
    portada=p.path_portada
    print "Contenido p.path_portada: "+portada
    if perfil=="imagenes/" or perfil=="imagenes/None":
        perfil="imagenes/sin_foto.jpg"
    if portada=="imagenes/" or portada=="imagenes/None":
        portada="imagenes/sin_portada.jpg"
    dic_imagenes={'perfil':perfil,'portada':portada}
    lista_dic_imagenes=[]
    lista_dic_imagenes.append(dic_imagenes)

    #Paso 9
    """comprobamos si el perfil que visualizamos somos nosotros, es un amigo o desconocido """
    somos_nosotros=False
    es_amigo=False
    peticion_enviada=False
    peticion_recibida=False
    if username == request.user.username:
        """ el perfil que vemos es el nuestro"""
        somos_nosotros=True
        print "somos nosotros"
    else:
        """comprobamos si es amigo"""
        for amigo in p.amigos.all(): 
            print "amigo:"+amigo.__unicode__()
            if amigo.user.username == request.user.username:
                print request.user.username+" es amigo de "+amigo.user.username
                es_amigo=True
        if es_amigo==False:
            """ si no es amigo tres casos:
                    - Le hemos mandado una peticion de amistad, luego deberiamos ver 'La peticion fue enviada'
                    - Hemos recibido una peticion suya, luego debemos ver 'Aceptar peticion' y 'Rechazar peticion'
                    - No hay peticiones entre ambos, no somos amigos, luego debemos ver 'Agregar como amigo'
            """
            print 'no son amigos'
            usuario_logueado= get_object_or_404(Perfil, user__username=request.user.username) 
            if PeticionAmistad.objects.filter(emisor=usuario_logueado, receptor=p):
                peticion_enviada=True
                print 'Existe peticion de '+usuario_logueado.user.username+' a '+p.user.username
            elif PeticionAmistad.objects.filter(emisor=p, receptor=usuario_logueado):
                peticion_recibida=True
                print 'Existe peticion de '+p.user.username+' a '+usuario_logueado.user.username
            else:
                print 'ni son amigos ni le envio la peticion'
            """
            else:
                print "no son amigos"
                #Buscar peticion emisor=request.user.username y receptor=amigo.user.username
                #Si la hay entonces imprimir Peticion Enviada sino Agregar amigo
                if PeticionAmistad.objects.filter(emisor=amigo.user.username, receptor=request.user.username):
                    peticion_enviada=True
                    print 'Existe peticion de '+request.user.username+' a '+amigo.user.username
                else:
                    print 'ni son amigos ni le envio la peticion'
            """
                    
    diccionario_amigos={"somos_nosotros":somos_nosotros,"es_amigo":es_amigo, 'peticion_enviada':peticion_enviada, 'peticion_recibida':peticion_recibida}
    print diccionario_amigos
    lista_dic_amigo=[]
    lista_dic_amigo.append(diccionario_amigos) #devolvemos lista con diccionario unico donde especifica si es amigo o no el perfil que visitamos
    
    amigos=p.amigos.all()
    grupos=list(Grupo.objects.filter(miembros__user__username=p.user.username))
    
    if somos_nosotros==False:
        formulario_respuesta=ComentarioForm()
        print "Somos nosotros es false no devolvemos formulario de comentar"
        context = {'lista_diccionario_comentarios': lista_diccionarios_def, 'formulario_respuesta':formulario_respuesta,'lista_dic_imagenes':lista_dic_imagenes, 'lista_dic_amigo':lista_dic_amigo, 'perfil':p, 'amigos':amigos, 'grupos':grupos}
    else:
        #Paso 8
        """ add form comentar"""
        formulario_respuesta=ComentarioForm()
        formulario=ComentarioForm()
        context = {'lista_diccionario_comentarios': lista_diccionarios_def, 'formulario':formulario,'formulario_respuesta':formulario_respuesta, 'lista_dic_imagenes':lista_dic_imagenes, 'lista_dic_amigo':lista_dic_amigo, 'perfil':p, 'amigos':amigos, 'grupos':grupos}
    return render_to_response('perfil.html',context,context_instance=RequestContext(request))

def comentarios_scroll(request):
    #comentarios = [i for i in Comentario.objects.all()]
    comentarios=list(Comentario.objects.values())
    paginator = Paginator(comentarios, 15)
    if request.method == 'GET':
        if request.is_ajax():
            if request.GET.get('page_number'):
                # Paginate based on the page number in the GET request
                page_number = request.GET.get('page_number');
                try:
                    page_objects = paginator.page(page_number).object_list
                except InvalidPage:
                    return HttpResponseBadRequest(mimetype="json")
                # Serialize the paginated objects
                #resp = serializers.serialize('json', page_objects)
                lista=[i for i in page_objects]
                print lista
                print "es lista"
                resp=lista
                #resp = serialize_comentarios(page_objects)
                #print json.dumps(resp)
                #return HttpResponse(json.dumps(resp))
                print JsonResponse(resp, safe=False)
                print "es json"
                return JsonResponse(resp, safe=False)
    comentarios = paginator.page(1).object_list
    context = {
        "object_list": comentarios,
    }
    return render_to_response('list.html', context,  context_instance=RequestContext(request))

@login_required(login_url='/login')
def home(request):
    #REvisar el bucle porque cuando no tiene amigos no muestra ni sus propios comentarios
    username=request.user.username
    #lista_comentarios=[]
    p = get_object_or_404(Perfil, user__username=username)
    """
    if p.amigos.all(): #si tiene amigos devolvemos los de sus amigos los suyos y actualizaciones en sus grupos
        print "TIENE AMIGOS"
        for amigo in p.amigos.all():
            comentarios=Comentario.objects.filter(Q(perfil=amigo)|Q(perfil=p)|Q(grupo__miembros__user__username=p.user.username)).order_by('fecha').reverse()
            for c in comentarios:
                lista_comentarios.append(c)
    else:#si no tiene amigos devolvemos los suyos y las actualizaciones en sus grupos
        comentarios=Comentario.objects.filter(Q(perfil=p)| Q(grupo__miembros__user__username=p.user.username)).order_by('fecha').reverse()
        for c in comentarios:
            lista_comentarios.append(c)
        print "NO TIENE AMIGOS"
    print lista_comentarios
    """
    #lista_comentarios=list(Comentario.objects.filter( Q(perfil=p) | Q(perfil__in=p.amigos.all()) | Q(grupo__miembros=p) ).order_by('fecha').reverse())
    """
    Mostramos:
    1- Actualizaciones nuestras
    2- Actualizaciones de nuestros amigos en ningun grupo
    3- Actualizaciones en nuestros grupos
    """
    lista_comentarios=list(Comentario.objects.filter( (Q(perfil=p) | Q(perfil__in=p.amigos.all(), grupo=None)) | Q(grupo__miembros=p)).distinct().order_by('fecha').reverse())
    print lista_comentarios
    paginator=Paginator(lista_comentarios,5)
    comentarios=paginator.page(1).object_list
    
    #context = {'lista_comentarios': lista_comentarios}
    formulario=ComentarioForm()
    context = {'comentarios': comentarios,'formulario':formulario, 'perfil':p}
    return render_to_response('home.html',context,context_instance=RequestContext(request))

def home_ajax(request): #No se para que recojo la variable username si luego la redefino
    username=request.user.username
    comentarios_list=[]
    p = get_object_or_404(Perfil, user__username=username)
    """
    if p.amigos.all(): #si tiene amigos devolvemos los de sus amigos los suyos y actualizaciones en sus grupos
        print "TIENE AMIGOS"
        for amigo in p.amigos.all():
            comentarios=Comentario.objects.filter(Q(perfil=amigo)|Q(perfil=p)|Q(grupo__miembros__user__username=p.user.username)).order_by('fecha').reverse()
            for c in comentarios:
                comentarios_list.append(c)
    else:#si no tiene amigos devolvemos los suyos y las actualizaciones en sus grupos
        comentarios=Comentario.objects.filter(Q(perfil=p)| Q(grupo__miembros__user__username=p.user.username)).order_by('fecha').reverse()
        for c in comentarios:
            comentarios_list.append(c)
        print "NO TIENE AMIGOS"
    """
    #lista_comentarios=Comentario.objects.filter((Q(perfil__amigos=p)|Q(perfil=p)),grupo__miembros=p).order_by('fecha').reverse()
    comentarios_list=list(Comentario.objects.filter( (Q(perfil=p) | Q(perfil__in=p.amigos.all(), grupo=None)) | Q(grupo__miembros=p)).distinct().order_by('fecha').reverse())
    
    print comentarios_list
    paginator=Paginator(comentarios_list,5)
    
    print("Entramos en perfil ajax")
    if request.is_ajax():
        if request.method=="GET":
            if request.GET.get("page_number"):
                print "entramos en get"
                page_number=request.GET.get('page_number')
                print page_number
                try:
                    comentarios=paginator.page(page_number).object_list
                except InvalidPage:
                    #return HttpResponseBadRequest(mimetype='json')
                    comentarios=[]
                lista_comentarios=[]
                print comentarios
                for c in comentarios:
                    dic_comentario={}
                    dic_comentario["id"]=c.id
                    dic_comentario["nombre"]=c.perfil.user.first_name
                    dic_comentario["username"]=c.perfil.user.username
                    dic_comentario["path_principal"]=c.perfil.path_principal
                    if c.grupo != None: #COMPROBAMOS SI EL GRUPO ES NONE
                        dic_comentario["grupo"]=c.grupo.__unicode__()
                    else:
                        dic_comentario["grupo"]=c.grupo
                    dic_comentario["fecha"]=c.fecha
                    dic_comentario["texto"]=c.texto
                    if c.partida != None:
                        dic_comentario["partida"]=c.partida.path
                    else:
                        dic_comentario["partida"]=""
                    resp=Respuesta.objects.filter(comentario=c)
                    lista_respuestas=[]
                    for r in resp:
                        dic_respuesta={"texto":r.texto,"fecha":r.fecha, "imagen_perfil":r.perfil.path_principal}
                        if r.partida != None:
                            dic_respuesta["partida"]=r.partida.path
                        else:
                            dic_respuesta["partida"]=""
                        lista_respuestas.append(dic_respuesta)
                    dic_comentario["respuestas"]=lista_respuestas
                    lista_comentarios.append(dic_comentario)
                print lista_comentarios
                return JsonResponse(lista_comentarios, safe=False)
                print "no se retorna"

@login_required(login_url='/login')
def home2(request):
    #REvisar el bucle porque cuando no tiene amigos no muestra ni sus propios comentarios
    username=request.user.username
    lista_comentarios=[]
    p = get_object_or_404(Perfil, user__username=username)
    if p.amigos.all(): #si tiene amigos devolvemos los de sus amigos los suyos y actualizaciones en sus grupos
        print "TIENE AMIGOS"
        for amigo in p.amigos.all():
            comentarios=Comentario.objects.filter(Q(perfil=amigo)|Q(perfil=p)|Q(grupo__miembros__user__username=p.user.username)).order_by('fecha').reverse()
            for c in comentarios:
                lista_comentarios.append(c)
    else:#si no tiene amigos devolvemos los suyos y las actualizaciones en sus grupos
        comentarios=Comentario.objects.filter(Q(perfil=p)| Q(grupo__miembros__user__username=p.user.username)).order_by('fecha').reverse()
        for c in comentarios:
            lista_comentarios.append(c)
        print "NO TIENE AMIGOS"
    print lista_comentarios
    
    lista_diccionario_comentarios_respuestas=[]
    for c in lista_comentarios:
        diccionario_comentarios_respuestas={}
        print "Comentario: "+c.__unicode__()
        # diccionario = {'comentario': r1, 'respuestas': [r1,r2,r3]}
        diccionario_comentarios_respuestas['comentario']=c
        resp=list(Respuesta.objects.filter(comentario=c))
        print resp
        diccionario_comentarios_respuestas['respuestas']=resp
        lista_diccionario_comentarios_respuestas.append(diccionario_comentarios_respuestas)

    print "Lista comentarios y respuestas: "
    print lista_diccionario_comentarios_respuestas
    
    #context = {'lista_comentarios': lista_comentarios}
    formulario=ComentarioForm()
    context = {'lista_dic_commentarios_respuestas': lista_diccionario_comentarios_respuestas,'formulario':formulario}
    return render_to_response('home.html',context,context_instance=RequestContext(request))
    
def crea_comentario(request):
    if request.is_ajax():
        #formulario=ComentarioForm(texto=request.POST['texto'])
        print request.POST
        print "request.Files"
        print request.FILES
        print request.POST
        print request.POST['url']
        if 'fichero' in request.FILES: #comprobamos que tenga fichero
            form = ComentarioForm(request.POST, request.FILES)
            if form.is_valid():
                print form
                print "Path_info: "+request.path_info
                #form.save()
                #comentario=form.save(commit=False)
                fecha=datetime.now()
                perfil=Perfil.objects.get(user=request.user)
                path_fichero=BASE_DIR+"/static/sgf/"+request.FILES['fichero'].__str__()
                print "path fichero:"+path_fichero
                
                """Intento de modificar nombre fichero y su path correspondiente YA NO ES NECESARIO PORQUE LO HACEMOS EN EL MODEL"""
                """
                fichero=request.FILES['fichero']
                print "nombre del fichero: "+fichero.name
                name=fichero.name
                nombre=name.split('.')
                nombre[0]=nombre[0]+"xyz" #add terminacion random
                fichero.name=nombre[0]+"."+nombre[1]
                print "nombre del fichero: "+fichero.name
                camino_fichero="sgf/"+fichero.name
                print camino_fichero
                """
                """ Fin intento modificar nombre fichero"""
                """ 
                for chunk in request.FILES['fichero'].chunks():
                    print chunk
                """
                """ Estamos leyendo la partida y sacando la informacion util para crearla"""
                lineas=request.FILES['fichero'].chunks()
                diccionario_informacion=informacion_partida2(lineas, path_fichero)
                print diccionario_informacion
                jugador_negro, created = Jugador.objects.get_or_create(nombre=diccionario_informacion['black'])
                #jugador_negro=Jugador(nombre=diccionario_informacion['black'])
                #jugador_negro.save()
                jugador_blanco, created = Jugador.objects.get_or_create(nombre=diccionario_informacion['blanco'])
                #jugador_blanco=Jugador(nombre=diccionario_informacion['blanco'])
                #jugador_blanco.save()
                """Seleccionamos path correcto"""
                cadenas=diccionario_informacion['path'].split("/")
                nombre_fichero=cadenas[len(cadenas)-1]
                path_fichero="sgf/"+nombre_fichero
                """Fin seleccionar path correcto"""
                partida = Partida(fecha=diccionario_informacion['fecha'], jugador_negro=jugador_negro, 
                                  jugador_blanco=jugador_blanco,rango_negro=diccionario_informacion['rango_negro'],rango_blanco=diccionario_informacion['rango_blanco'], resultado=diccionario_informacion['result'], 
                                  fichero=request.FILES['fichero'])
                partida.save()
                #print partida.__unicode__()
                #print 'partida salvada con exito'
                """ Fin crear la partida """
                perfil=perfil
                partida=partida
                texto=form.cleaned_data['texto']
                """Comprobamos si estamos en un grupo"""
                url=request.POST['url']
                lista=estamos_en_grupo(url)
                if lista[0]==True:
                    g=lista[1]
                    comentario=Comentario(fecha=fecha, perfil=perfil, texto=texto, partida=partida, grupo=g)
                else:
                    comentario=Comentario(fecha=fecha, perfil=perfil, texto=texto, partida=partida)
                """Fin comprobar si es un grupo"""
                comentario.save()
                #print 'comentario guardado con exito'
                comentarios=list(Comentario.objects.values())
                return JsonResponse(comentarios, safe=False)
            else:
                print "el formulario no es valido"
                print request.POST
                print request.FILES
        else:#no adjuntamos fichero
            form = ComentarioForm(request.POST)
            print form
            if form.is_valid():
                print "Path_info: "+request.path_info
                print "JEJEJEJEJEJ"
                fecha=datetime.now()
                print "FEcha: "+fecha.__str__()
                perfil=Perfil.objects.get(user=request.user)
                texto=form.cleaned_data['texto']
                """Comprobamos si estamos en un grupo"""
                url=request.POST['url']
                lista=estamos_en_grupo(url)
                if lista[0]==True:
                    g=lista[1]
                    comentario=Comentario(fecha=fecha, perfil=perfil, texto=texto, grupo=g)
                else:
                    comentario=Comentario(fecha=fecha, perfil=perfil, texto=texto)
                """Fin comprobar si es un grupo"""
                comentario.save()
                print "comentario guardado con exito"
                comentarios=list(Comentario.objects.values())
                return JsonResponse(comentarios, safe=False)
            else:
                print "no se contenia fichero pero el formulario no era valido"
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

def responder(request):
    if request.is_ajax():
        #formulario=ComentarioForm(texto=request.POST['texto'])
        print request.POST
        print "request.Files"
        print request.FILES
        print request.POST
        print request.POST['url']
        print "Id del comentario al que add la respuesta: "+request.POST["id_comentario"]
        id_comentario=int(request.POST["id_comentario"])
        if 'fichero' in request.FILES: #comprobamos que tenga fichero
            form = ComentarioForm(request.POST, request.FILES)
            if form.is_valid():
                print form
                print "Path_info: "+request.path_info
                #form.save()
                #comentario=form.save(commit=False)
                
                fecha=datetime.now()
                perfil=Perfil.objects.get(user=request.user)
                
                path_fichero=BASE_DIR+"/static/sgf/"+request.FILES['fichero'].__str__()
                print "path fichero:"+path_fichero
    
                """ 
                for chunk in request.FILES['fichero'].chunks():
                    print chunk
                """
                """ Estamos leyendo la partida y sacando la informacion util para crearla"""
                lineas=request.FILES['fichero'].chunks()
                diccionario_informacion=informacion_partida2(lineas, path_fichero)
                print diccionario_informacion 
                """Seleccionamos path correcto NO ES NECESARIO PORQUE LO HACEMOS EN EL MODEL"""
                """
                cadenas=diccionario_informacion['path'].split("/")
                nombre_fichero=cadenas[len(cadenas)-1]
                path_fichero="sgf/"+nombre_fichero
                """
                """fin seleccionar path correcto"""
                jugador_negro, created = Jugador.objects.get_or_create(nombre=diccionario_informacion['black'])
                #jugador_negro=Jugador(nombre=diccionario_informacion['black'])
                #jugador_negro.save()
                print 'jugador negro guardado con exito'
                jugador_blanco, created = Jugador.objects.get_or_create(nombre=diccionario_informacion['blanco'])
                #jugador_blanco=Jugador(nombre=diccionario_informacion['blanco'])
                #jugador_blanco.save()
                partida = Partida(fecha=diccionario_informacion['fecha'], jugador_negro=jugador_negro, 
                                  jugador_blanco=jugador_blanco,rango_negro=diccionario_informacion['rango_negro'],rango_blanco=diccionario_informacion['rango_blanco'], resultado=diccionario_informacion['result'], 
                                  fichero=request.FILES['fichero'])
                partida.save()
                print partida.__unicode__()
                print 'partida salvada con exito'
                """ Fin crear la partida """
                perfil=perfil
                partida=partida
                texto=form.cleaned_data['texto']
                comentario=Comentario.objects.get(id=id_comentario)
                print "Comentario al que respondemos: "+comentario.__unicode__()
                respuesta=Respuesta(fecha=fecha, perfil=perfil, texto=texto, partida=partida, comentario=comentario)
                respuesta.save()
                print 'respuesta guardada con exito'
                comentarios=list(Comentario.objects.values())
                return JsonResponse(comentarios, safe=False)
            else:
                print "el formulario no es valido"
                print request.POST
                print request.FILES
        else:#no adjuntamos fichero
            form = ComentarioForm(request.POST)
            print form
            if form.is_valid():
                print "Path_info: "+request.path_info
                print "JEJEJEJEJEJ"
                fecha=datetime.now()
                print "FEcha: "+fecha.__str__()
                perfil=Perfil.objects.get(user=request.user)
                texto=form.cleaned_data['texto']
                comentario=Comentario.objects.get(id=id_comentario)
                print "Comentario al que respondemos: "+comentario.__unicode__()
                respuesta=Respuesta(fecha=fecha, perfil=perfil, texto=texto, comentario=comentario)
                respuesta.save()
                print "Respuesta guardada con exito"
                comentarios=list(Comentario.objects.values())
                return JsonResponse(comentarios, safe=False)
            else:
                print "no se contenia fichero pero el formulario no era valido"
    else:
        print "ENTRAMOS EN ELSE AL NO SER AJAX"
        return HttpResponseRedirect(request.META['HTTP_REFERER'])

def buscador(request):
    if request.is_ajax():
        if request.method=='GET':
            print "Esto contiene request.GET: "+request.GET['texto']
            cadena=request.GET['texto']
            #usaremos irregex para diferenciar entre minusculas y mayusculas
            
            if cadena!="":
                lista_perfiles=list(Perfil.objects.values('user__first_name', 'user__last_name', 'user__username','path_principal').filter(Q(user__first_name__iregex=cadena) | Q(user__last_name__iregex=cadena))) #cambiar username por first_name o last_nameprint lista_perfiles
                lista_grup=list(Grupo.objects.values('id', 'titulo').filter(titulo__iregex=cadena))
                print lista_grup
                print lista_perfiles
                lista_res=[]
                lista_res.append(lista_perfiles)
                lista_res.append(lista_grup)
                print lista_res
                print JsonResponse(lista_res, safe=False)
                #print JsonResponse(lista_perfiles, safe=False)
                return JsonResponse(lista_res, safe=False)
            else:
                lista_perfiles=[]
                return JsonResponse(lista_perfiles, safe=False)
            """
            print lista_perfiles
            context={'lista_perfiles',lista_perfiles}
            return render_to_response('busqueda.html', context, context_instance=RequestContext(request))
            """
        else:
            render("Hubo un problema en su peticion")
    else:
        lista_grup=[]
        lista_perfiles=[]
        print "no es una peticion ajax"
        print request.GET
        if request.method=='POST':
            print "Esto contiene request.POST: "+request.POST['buscar_texto']
            cadena=request.POST['buscar_texto']
            #usaremos irregex para diferenciar entre minusculas y mayusculas
            if cadena!="":
                lista_perfiles=list(Perfil.objects.filter(Q(user__first_name__iregex=cadena) | Q(user__last_name__iregex=cadena))) #cambiar username por first_name o last_nameprint lista_perfiles
                lista_grup=list(Grupo.objects.filter(titulo__iregex=cadena))
            context={'lista_perfiles':lista_perfiles, 'lista_grupos':lista_grup}
            print context
            return render_to_response('busqueda.html', context, context_instance=RequestContext(request))

        #return HttpResponseRedirect(request.META['HTTP_REFERER']) #Asi recargariamos la página

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

def eliminar_ajax(request):
    if request.is_ajax():
        if request.method=='GET':
            username_amigo=request.GET['perfil_para_eliminar']
            yo=get_object_or_404(Perfil, user__username=request.user.username)
            amigo=get_object_or_404(Perfil, user__username=username_amigo)
            yo.amigos.remove(amigo)
            yo.save()
            print "eliminado con exito"
            return HttpResponse("Eliminado con éxito")
    else:
        return HttpResponse("Problema con peticion ajax")

def contar_notificaciones(request):
    if request.is_ajax():
        if request.method=='GET':
            recuento_peticiones = PeticionAmistad.objects.filter(receptor__user__username=request.user.username).count()
            recuento_notificaciones=Notificacion.objects.filter(receptor__user__username=request.user.username).count()
            recuento=recuento_notificaciones+recuento_peticiones
            print "Recuento: "+recuento.__str__()
            return HttpResponse(recuento)
    else:
        print "no es peticion ajax o GET"
        return HttpResponse("no es peticion ajax o GET")

def ver_notificaciones(request):
    lista_peticiones=list(PeticionAmistad.objects.filter(receptor__user__username=request.user.username))
    lista_notificaciones=list(Notificacion.objects.filter(receptor__user__username=request.user.username))
    lista_peticiones_revision=list(PeticionRevision.objects.filter(receptor__user__username=request.user.username))
    form=SgfForm()
    context={'lista_peticiones': lista_peticiones, 'lista_notificaciones': lista_notificaciones, 'form':form, 'lista_peticiones_revision': lista_peticiones_revision}
    print context
    return render_to_response('notificaciones.html',context,context_instance=RequestContext(request))


def aceptar_peticion(request):
    if request.is_ajax():
        if request.method=='POST':
            print "Entramos en Ajax y GET"
            emisor=get_object_or_404(Perfil, user__username=request.POST['nick']) #es el emisor de la peticion de amistad
            receptor=get_object_or_404(Perfil, user__username=request.user.username) #es el receptor de la peticion de amistad
            receptor.amigos.add(emisor) #con add en uno al otro ya es mutuo
            receptor.save()
            mensaje=receptor.user.first_name+" "+receptor.user.last_name+" acepto tu peticion de amistad"
            notificacion=Notificacion(receptor=emisor, mensaje=mensaje)
            notificacion.save() #creamos notificacion que visualizara el emisor de la peticion de amistad de que el receptor la acepto
            peticion=PeticionAmistad.objects.get(emisor=emisor, receptor=receptor)
            peticion.delete() #borramos la peticion de amistad
            cadena=emisor.user.first_name+" "+emisor.user.last_name+" es ahora tu amigo."
            return HttpResponse(cadena)
    else:
        return HttpResponse("Error con la peticion ajax")

def declinar_peticion(request):
    if request.is_ajax():
        if request.method=='GET':
            emisor=get_object_or_404(Perfil, user__username=request.GET['nick'])
            receptor=get_object_or_404(Perfil, user__username=request.user.username)
            peticion=PeticionAmistad.objects.get(emisor=emisor, receptor=receptor)
            peticion.delete()
            cadena="La peticion ha sido rechazada con éxito"
            return HttpResponse(cadena)
    else:
        return HttpResponse('Error con la peticion ajax')

def limpiar_notificaciones(request):
    if request.is_ajax():
        if request.method=='GET':
            boton = request.GET['boton']
            receptor= get_object_or_404(Perfil, user__username=request.user.username)
            if boton=='limpiar_notificaciones':
                Notificacion.objects.filter(receptor=receptor).delete()
            elif boton=='limpiar_peticiones':
                PeticionAmistad.objects.filter(receptor=receptor).delete()
            return HttpResponse("Se borraron correctamente.")
    else:
        return HttpResponse('Error en la peticion Ajax')
           
def grupo(request, grupo_id):
    g = get_object_or_404(Grupo, pk=grupo_id)
    comentarios_filter=list(Comentario.objects.filter(grupo=g).order_by('fecha').reverse())
    paginator=Paginator(comentarios_filter,5)
    lista_comentarios=paginator.page(1).object_list
    if request.is_ajax():
        if request.method=="GET":
            if request.GET.get("page_number"):
                page_number=request.GET.get('page_number')
                try:
                    comentarios=paginator.page(page_number).object_list
                except InvalidPage:
                    comentarios=[]
                lista_comentarios=[]
                for c in comentarios:
                    dic_comentario={}
                    dic_comentario["id"]=c.id
                    dic_comentario["nombre"]=c.perfil.user.first_name
                    dic_comentario["username"]=c.perfil.user.username
                    dic_comentario["path_principal"]=c.perfil.path_principal
                    if c.grupo != None: #COMPROBAMOS SI EL GRUPO ES NONE
                        dic_comentario["grupo"]=c.grupo.__unicode__()
                    else:
                        dic_comentario["grupo"]=c.grupo
                    dic_comentario["fecha"]=c.fecha
                    dic_comentario["texto"]=c.texto
                    if c.partida != None:
                        dic_comentario["partida"]=c.partida.path
                    else:
                        dic_comentario["partida"]=""
                    resp=Respuesta.objects.filter(comentario=c)
                    lista_respuestas=[]
                    for r in resp:
                        dic_respuesta={"texto":r.texto,"fecha":r.fecha, "imagen_perfil":r.perfil.path_principal}
                        if r.partida != None:
                            dic_respuesta["partida"]=r.partida.path
                        else:
                            dic_respuesta["partida"]=""
                        lista_respuestas.append(dic_respuesta)
                    dic_comentario["respuestas"]=lista_respuestas
                    lista_comentarios.append(dic_comentario)
                print lista_comentarios
                return JsonResponse(lista_comentarios, safe=False)
    """ add form comentar"""
    formulario=ComentarioForm()
    """ comprobamos si el usuario es miembro o no del grupo """
    miembro=False
    p=get_object_or_404(Perfil, user__username=request.user.username)
    if g.miembros.filter(user__username=p.user.username):
        print "Somos miembros"
        miembro=True
    context = {'comentarios': lista_comentarios, 'formulario':formulario, 'grupo':g ,'miembro':miembro}
    return render_to_response('grupo.html',context,context_instance=RequestContext(request))


def grupo2(request, grupo_id):
    print request.user
    lista_diccionarios_def=[]
    g = get_object_or_404(Grupo, pk=grupo_id)
    print g.__unicode__()
    diccionario_grupo_comentarios={}
    diccionario_grupo_comentarios["grupo"]=g 
    comentarios=Comentario.objects.filter(grupo=g).order_by('fecha').reverse()
    print comentarios
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
    diccionario_grupo_comentarios['comentarios']=lista_diccionario_comentarios_respuestas
    lista_diccionarios_def.append(diccionario_grupo_comentarios)
    print lista_diccionarios_def
    
    """ add form comentar"""
    formulario=ComentarioForm()
    
    """ add nombre del grupo - path portada - descripcion """
    titulo=g.titulo
    path_portada=g.path_portada
    descripcion=g.descripcion
    """ comprobamos si el usuario es miembro o no del grupo """
    miembro=False
    p=get_object_or_404(Perfil, user__username=request.user.username)
    if g.miembros.filter(user__username=p.user.username):
        print "Somos miembros"
        miembro=True
    
    
    context = {'lista_diccionario_comentarios': lista_diccionarios_def, 'formulario':formulario, 'titulo':titulo, 'path_portada':path_portada, 'miembro':miembro, 'descripcion':descripcion}
    return render_to_response('grupo.html',context,context_instance=RequestContext(request))

def lista_grupos(request):
    p=get_object_or_404(Perfil, user__username=request.user.username)
    print p
    grupos=list(Grupo.objects.values('titulo','descripcion','pk').filter(miembros__user__username=p.user.username))
    print grupos
    form=GrupoForm()
    context = {'lista_grupos': grupos,'form':form}
    return render_to_response('lista_grupos.html',context,context_instance=RequestContext(request))

def amigos(request):
    p=get_object_or_404(Perfil, user__username=request.user.username)
    amigos=list(p.amigos.all())
    
    """ add perfiles recomendados """
    diccionario_amigos=perfiles_amigos()
    lista_recomendacion_comun=topMatches_amigos_comun(diccionario_amigos, p)
    
    diccionario_gustos=perfiles_gustos()
    lista_recomendacion_gustos=topMatches_gustos(diccionario_gustos, p)
    """ fin perfiles recomendados"""
    
    context = {'lista_amigos': amigos, 'lista_recomendacion_comun': lista_recomendacion_comun, 'lista_recomendacion_gustos': lista_recomendacion_gustos}
    return render_to_response('amigos.html', context, context_instance=RequestContext(request))

def partidas(request):
    partidas_p=list(PartidaRepositorio.objects.filter(es_profesional=True).order_by('fecha').reverse())
    paginator_p = Paginator(partidas_p, 10)
    lista_partidas_profesionales=paginator_p.page(1).object_list
    
    partidas_a=list(PartidaRepositorio.objects.filter(es_profesional=False).order_by('fecha').reverse())
    paginator_a = Paginator(partidas_a, 10)
    lista_partidas_amateur=paginator_a.page(1).object_list
    
    """ Devolvemos diccionario con todos los jugadores del sistema nombres de jugadores"""
    dic_jugadores_p={}
    dic_jugadores_a={}
    abecedario= ["A", "B", "C", "D", "E", "F", "G","H","I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]
    for letra in abecedario:
        lista_p=[]
        lista_a=[]
        for j in Jugador.objects.filter(nombre__startswith=letra):
            if j.es_profesional==True:
                lista_p.append(j)
            else:
                lista_a.append(j)
        dic_jugadores_p[letra]=lista_p
        dic_jugadores_a[letra]=lista_a
    
    """ Fin devolver diccionario jugadores """
    form=SgfForm()
    form_fecha=FechasForm()
    context ={'lista_partidas_profesionales':lista_partidas_profesionales, 'lista_partidas_amateur':lista_partidas_amateur,'dic_jugadores_p':dic_jugadores_p, 'dic_jugadores_a':dic_jugadores_a, 'form':form, 'form_fecha':form_fecha}
    return render_to_response('partidas.html', context, context_instance=RequestContext(request))
    
def partidas_ajax(request):
    #partidas=list(Partida.objects.values().order_by('fecha').reverse())
    partidas=list(Partida.objects.all().order_by('fecha').reverse())
    paginator = Paginator(partidas, 10)
    if request.is_ajax():
        if request.method=="GET":
            if request.GET.get('page_number'):
                # Paginate based on the page number in the GET request
                page_number = request.GET.get('page_number');
                print "Entramos en Partidas_Ajax"
                print page_number
                try:
                    page_objects = paginator.page(page_number).object_list
                    print page_objects
                except InvalidPage:
                    #return HttpResponseBadRequest(mimetype="json")
                    #puede ser que al ser multiplo de 10 ya no queden elementos en la pagina siguiente. Devolvemos lista vacia
                    page_objects=[]
                lista=[i for i in page_objects]
                #return JsonResponse(serializers.serialize('json',lista, use_natural_foreign_keys=True, safe=False)) esta opcion no funcionaba pusieramos en el codigo javascript que recibiamos json como si no
                print HttpResponse(serializers.serialize('json',lista, use_natural_foreign_keys=True))
                return HttpResponse(serializers.serialize('json',lista, use_natural_foreign_keys=True))
            
def partidas_jugador(request, id):
    partidas=list(Partida.objects.filter(Q(jugador_negro__id=id) | Q(jugador_blanco__id=id)))
    jugador=Jugador.objects.get(id=id)
    context={'partidas': partidas, 'jugador':jugador.nombre}
    return render_to_response('jugador.html', context, context_instance=RequestContext(request))

def revisiones(request):
    partidas=list(Partida.objects.exclude(revisor=None).order_by('fecha').reverse())
    paginator = Paginator(partidas, 2)
    if request.is_ajax():
        if request.method=="GET":
            page_number = request.GET.get('page_number');
            try:
                page_objects = paginator.page(page_number).object_list
            except InvalidPage:
                page_objects=[]
            lista_partidas=[]
            for p in page_objects:
                dic_partida={}
                dic_partida["revisor_nickname"]=p.revisor.nickname_kgs
                dic_partida["revisor_rango"]=p.revisor.perfil.rango
                dic_partida["jugador_negro_nombre"]=p.jugador_negro.nombre
                dic_partida["jugador_negro_id"]=p.jugador_negro.id
                dic_partida["jugador_blanco_nombre"]=p.jugador_blanco.nombre
                dic_partida["jugador_blanco_id"]=p.jugador_blanco.id
                dic_partida["rango_negro"]=p.rango_negro
                dic_partida["rango_blanco"]=p.rango_blanco
                dic_partida["fecha"]=p.fecha
                dic_partida["resultado"]=p.resultado
                dic_partida["partida_id"]=p.id
                lista_partidas.append(dic_partida)
            print lista_partidas
            return JsonResponse(lista_partidas, safe=False)        
    else:
        soy_revisor=False
        p=Perfil.objects.get(user__username=request.user.username)
        if Revisor.objects.filter(perfil=p):
            soy_revisor=True
        name='revisiones.html'
        lista=paginator.page(1).object_list
        revisores=list(Revisor.objects.all())
        form=EnvioForm()
        #form.fields['revisor']=forms.Revisor.objects.all()
        context={'partidas_revisadas':lista, 'form':form, 'revisores': revisores, 'soy_revisor':soy_revisor}
        return render(request,name, context)

def partidas_by_revisor(request, nickname_kgs):
    print "Se llama a partidas_by_revisor"
    partidas=list(Partida.objects.filter(revisor__nickname_kgs=nickname_kgs).order_by('fecha').reverse())
    paginator = Paginator(partidas, 2)
    if request.is_ajax():
        if request.method=="GET":
            page_number = request.GET.get('page_number');
            try:
                if page_number>1:
                    page_objects = paginator.page(page_number).object_list
                else:
                    page_objects = paginator.page(1).object_list
            except InvalidPage:
                page_objects=[]
            lista_partidas=[]
            for p in page_objects:
                dic_partida={}
                dic_partida["revisor_nickname"]=p.revisor.nickname_kgs
                dic_partida["revisor_rango"]=p.revisor.perfil.rango
                dic_partida["jugador_negro_nombre"]=p.jugador_negro.nombre
                dic_partida["jugador_negro_id"]=p.jugador_negro.id
                dic_partida["jugador_blanco_nombre"]=p.jugador_blanco.nombre
                dic_partida["jugador_blanco_id"]=p.jugador_blanco.id
                dic_partida["rango_negro"]=p.rango_negro
                dic_partida["rango_blanco"]=p.rango_blanco
                dic_partida["fecha"]=p.fecha
                dic_partida["resultado"]=p.resultado
                dic_partida["partida_id"]=p.id
                lista_partidas.append(dic_partida)
            print lista_partidas
            return JsonResponse(lista_partidas, safe=False)
    else:
        name='by_revisor.html'
        lista=list(Partida.objects.filter(revisor__nickname_kgs=nickname_kgs))
        context={'partidas_revisadas':lista}
        return render(request, name, context)
    """
    name='by_revisor.html'
    lista=list(Partida.objects.filter(revisor__nickname_kgs=nickname_kgs))
    context={'partidas_revisadas':lista}
    return render(request, name, context)
    """

def crear_grupo(request):
    if request.method=="POST":
        if 'foto_portada' in request.FILES: #comprobamos que tenga fichero
            form = GrupoForm(request.POST, request.FILES)
            print form
            if form.is_valid():
                titulo=form.cleaned_data['titulo']
                descripcion=form.cleaned_data['descripcion']
                foto_portada=form.cleaned_data['foto_portada']
                path_portada='imagenes'+foto_portada.name
                grupo, created=Grupo.objects.get_or_create(titulo=titulo, descripcion=descripcion, foto_portada=foto_portada, path_portada=path_portada)
                perfil=Perfil.objects.get(user__username=request.user.username)
                grupo.miembros.add(perfil)
                grupo.save()
                return HttpResponseRedirect(request.META['HTTP_REFERER'])
            else:
                print "el fichero con imagen no es valido"
        else:
            form = GrupoForm(request.POST)
            print form
            if form.is_valid():
                titulo=form.cleaned_data['titulo']
                descripcion=form.cleaned_data['descripcion']
                grupo, created=Grupo.objects.get_or_create(titulo=titulo, descripcion=descripcion)
                print grupo
                perfil=Perfil.objects.get(user__username=request.user.username)
                print perfil
                grupo.miembros.add(perfil)
                #receptor.amigos.add(emisor)
                grupo.save()
                return HttpResponseRedirect(request.META['HTTP_REFERER'])
            else:
                print "el formulario sin imagen no es valido"
    else:
        print "el metodo no es POST"

#Sistema de revisiones de partidas
def enviar_partida_revisar(request):
    form = EnvioForm(request.POST, request.FILES)
    if form.is_valid():
        p=Perfil.objects.get(user__username=request.user.username)
        revisor=Revisor.objects.get(id=request.POST['revisor'])
        if not PeticionRevision.objects.filter(receptor=revisor.perfil, emisor=p):
            print form
            """ Estamos leyendo la partida y sacando la informacion util para crearla"""
            path_fichero=BASE_DIR+"/static/sgf/"+request.FILES['fichero'].__str__()
            lineas=request.FILES['fichero'].chunks()
            diccionario_informacion=informacion_partida2(lineas, path_fichero)
            print diccionario_informacion 
            jugador_negro, created = Jugador.objects.get_or_create(nombre=diccionario_informacion['black'])
            #jugador_negro=Jugador(nombre=diccionario_informacion['black'])
            #jugador_negro.save()
            print 'jugador negro guardado con exito'
            jugador_blanco, created = Jugador.objects.get_or_create(nombre=diccionario_informacion['blanco'])
            #jugador_blanco=Jugador(nombre=diccionario_informacion['blanco'])
            #jugador_blanco.save()
            partida = Partida(fecha=diccionario_informacion['fecha'], jugador_negro=jugador_negro, 
                              jugador_blanco=jugador_blanco, rango_negro=diccionario_informacion['rango_negro'],rango_blanco=diccionario_informacion['rango_blanco'], resultado=diccionario_informacion['result'], 
                              fichero=request.FILES['fichero'])
            partida.save()
            print partida.__unicode__()
            print 'partida salvada con exito'
            """ Fin crear la partida """
            """Mandamos las notificaciones"""
            
            print request.POST['revisor']
            
            mensaje_a_revisor="Tienes una nueva partida para revisar, puedes descargarla aqui: <a href='/static/"+partida.path+"'>Descargar</a>."
            peticion=PeticionRevision(receptor=revisor.perfil, emisor=p, mensaje=mensaje_a_revisor, revision=True)
            peticion.save()
            
            notificacion2=Notificacion(receptor=p, mensaje="Tu partida ha sido asignada con éxito, te rogamos esperes unos días antes de volver a enviarla a otro revisor.")
            notificacion2.save()
            print "Notificaciones enviadas con exito"
            return ver_notificaciones(request) #ESTO HAY QUE CAMBIARLO
        else:
            print "Ya existe una revision pendiente"
            return ver_notificaciones(request)
    else:
        print "el formulario no es valido"

def aceptar_partida_revisar(request, username):
    #aqui ya mandamos la partida suponemos que acepta si la revisa y sino la va a revisar rechazara cuando lea la notificacion
    revisor=Revisor.objects.get(perfil__user__username=request.user.username)
    form = SgfForm(request.POST, request.FILES)
    if form.is_valid():
        print form
        """ Estamos leyendo la partida y sacando la informacion util para crearla"""
        path_fichero=BASE_DIR+"/static/sgf/"+request.FILES['fichero'].__str__()
        lineas=request.FILES['fichero'].chunks()
        diccionario_informacion=informacion_partida2(lineas, path_fichero)
        print diccionario_informacion 
        jugador_negro, created = Jugador.objects.get_or_create(nombre=diccionario_informacion['black'])
        #jugador_negro=Jugador(nombre=diccionario_informacion['black'])
        #jugador_negro.save()
        print 'jugador negro guardado con exito'
        jugador_blanco, created = Jugador.objects.get_or_create(nombre=diccionario_informacion['blanco'])
        #jugador_blanco=Jugador(nombre=diccionario_informacion['blanco'])
        #jugador_blanco.save()
        partida = Partida(fecha=diccionario_informacion['fecha'], jugador_negro=jugador_negro, 
                          jugador_blanco=jugador_blanco, rango_negro=diccionario_informacion['rango_negro'],rango_blanco=diccionario_informacion['rango_blanco'], resultado=diccionario_informacion['result'], 
                          fichero=request.FILES['fichero'], revisor=revisor)
        partida.save()
        print partida.__unicode__()
        print 'partida salvada con exito'
        """ Fin crear la partida """
        """Mandamos las notificaciones"""
        mensaje_a_usuario="La partida ha sido revisada, puedes descargarla aqui: <a href='/static/"+partida.path+"'>Descargar</a>. O visualizarla desde el apartado de Revisiones"
        p=Perfil.objects.get(user__username=username)
        notificacion1=Notificacion(receptor=p, mensaje=mensaje_a_usuario)
        notificacion1.save()
        notificacion2=Notificacion(receptor=revisor.perfil, mensaje="La partida revisada fue almacenada con éxito en el sistema")
        notificacion2.save()
        peticion=PeticionRevision.objects.get(receptor=revisor.perfil, emisor=p)
        peticion.delete()
        return ver_notificaciones(request)
        print "Notificaciones enviadas con exito"
    else:
        print "el formulario no es valido"

def rechazar_partida_revisar(request):
    pass

def reenvio_partida_revisar(request):
    pass

def ver_partida(request, partida_id):
    partida=get_object_or_404(Partida, pk=partida_id)
    name="ver_partida.html"
    context={'partida':partida}
    return render(request,name, context)

def eliminar_comentario_ajax(request):
    if request.is_ajax():
        if request.method=='POST':
            comentario_id=request.POST['comentario_id']
            comentario=get_object_or_404(Comentario, pk=comentario_id)
            comentario.delete()
            print "eliminado con exito"
            return HttpResponse("Eliminado con éxito")
    else:
        return HttpResponse("Problema con peticion ajax")

#AUN SIN COMPROBAR
def crear_partida_repositorio(request):
    if request.method=='POST':
        profesionales=["1p", "2p", "3p", "4p", "5p", "6p", "7p", "8p", "9p"]
        path_fichero=BASE_DIR+"/static/sgf/"+request.FILES['fichero'].__str__()
        lineas=request.FILES['fichero'].chunks()
        diccionario_informacion=informacion_partida2(lineas, path_fichero)
        print diccionario_informacion
        jugador_negro, created = Jugador.objects.get_or_create(nombre=diccionario_informacion['black'])
        jugador_blanco, created = Jugador.objects.get_or_create(nombre=diccionario_informacion['blanco'])
        partida = PartidaRepositorio(fecha=diccionario_informacion['fecha'], jugador_negro=jugador_negro, 
                          jugador_blanco=jugador_blanco,rango_negro=diccionario_informacion['rango_negro'],rango_blanco=diccionario_informacion['rango_blanco'], resultado=diccionario_informacion['result'], 
                          fichero=request.FILES['fichero'])
        if partida.rango_negro in profesionales:
            jugador_negro.es_profesional=True
            jugador_negro.save()
            partida.es_profesional=True
        if partida.rango_blanco in profesionales:
            jugador_blanco.es_profesional=True
            jugador_blanco.save()
            partida.es_profesional=True
        partida.save()
        print partida.__unicode__()
        print 'partida salvada con exito'
        """ Fin crear la partida """
        #return HttpResponse("Ha sido un exito")
        name="partidas.html"
        context={}
        return render(request,name, context)
    else:
        print "no entramos en POST"


def unirse_revisor(request):
    if request.is_ajax():
        if request.method=='POST':
            print request.POST
            p=Perfil.objects.get(user__username=request.user.username)
            revisor=Revisor(perfil=p, nickname_kgs=request.POST['nick'])
            revisor.save()
            print revisor.__unicode__()
            return HttpResponse("Ha sido un exito")
def dejar_revisor(request):
    if request.is_ajax():
        if request.method=='GET':
            p=Perfil.objects.get(user__username=request.user.username)
            revisor=Revisor.objects.get(perfil=p)
            revisor.delete()
            return HttpResponse("Ha sido un exito")

def fuerza_revisor(request):  
    if request.is_ajax():
        if request.method=="GET":
            page_number = request.GET.get('page_number');
            try:
                rango_revisor=request.GET.get('rango')
                partidas=list(Partida.objects.filter(revisor__perfil__rango=rango_revisor).order_by('fecha').reverse())
                paginator = Paginator(partidas, 2)
                if page_number>1:
                    page_objects = paginator.page(page_number).object_list
                else:
                    page_objects = paginator.page(1).object_list
            except InvalidPage:
                page_objects=[]
            lista_partidas=[]
            for p in page_objects:
                dic_partida={}
                dic_partida["revisor_nickname"]=p.revisor.nickname_kgs
                dic_partida["revisor_rango"]=p.revisor.perfil.rango
                dic_partida["jugador_negro_nombre"]=p.jugador_negro.nombre
                dic_partida["jugador_negro_id"]=p.jugador_negro.id
                dic_partida["jugador_blanco_nombre"]=p.jugador_blanco.nombre
                dic_partida["jugador_blanco_id"]=p.jugador_blanco.id
                dic_partida["rango_negro"]=p.rango_negro
                dic_partida["rango_blanco"]=p.rango_blanco
                dic_partida["fecha"]=p.fecha
                dic_partida["resultado"]=p.resultado
                dic_partida["partida_id"]=p.id
                lista_partidas.append(dic_partida)
            print lista_partidas
            return JsonResponse(lista_partidas, safe=False)

def fuerza_jugador(request):
        if request.is_ajax():
            if request.method=="GET":
                page_number = request.GET.get('page_number');
                try:
                    rango_jugador=request.GET.get('rango')
                    partidas=list(Partida.objects.filter(Q(rango_negro=rango_jugador)|Q(rango_blanco=rango_jugador)).exclude(revisor=None).order_by('fecha').reverse())
                    print partidas
                    paginator = Paginator(partidas, 2)
                    if page_number>1:
                        print "entro page_number mayor 1"
                        page_objects = paginator.page(page_number).object_list
                    else:
                        print "entro en else"
                        page_objects = paginator.page(1).object_list
                except InvalidPage:
                    page_objects=[]
                print page_objects
                lista_partidas=[]
                for p in page_objects:
                    dic_partida={}
                    dic_partida["revisor_nickname"]=p.revisor.nickname_kgs
                    dic_partida["revisor_rango"]=p.revisor.perfil.rango
                    dic_partida["jugador_negro_nombre"]=p.jugador_negro.nombre
                    dic_partida["jugador_negro_id"]=p.jugador_negro.id
                    dic_partida["jugador_blanco_nombre"]=p.jugador_blanco.nombre
                    dic_partida["jugador_blanco_id"]=p.jugador_blanco.id
                    dic_partida["rango_negro"]=p.rango_negro
                    dic_partida["rango_blanco"]=p.rango_blanco
                    dic_partida["fecha"]=p.fecha
                    dic_partida["resultado"]=p.resultado
                    dic_partida["partida_id"]=p.id
                    lista_partidas.append(dic_partida)
                print lista_partidas
                return JsonResponse(lista_partidas, safe=False)

def recargar_repositorio_ajax(request):
    if request.is_ajax():
        if request.method=="GET":
            if request.GET.get('page_number'):
                if request.GET.get('profesional'):
                    partidas=list(PartidaRepositorio.objects.filter(es_profesional=True).order_by('fecha').reverse())
                    paginator = Paginator(partidas, 10)
                    print "recargamos las profesionales"
                else: #pedimos recargar el amateur
                    partidas=list(PartidaRepositorio.objects.filter(es_profesional=False).order_by('fecha').reverse())
                    paginator = Paginator(partidas, 10)
                    print "recargamos las amateur"
                page_number = request.GET.get('page_number');
                print page_number
                try:
                    page_objects = paginator.page(page_number).object_list
                    print page_objects
                except InvalidPage:
                    #return HttpResponseBadRequest(mimetype="json")
                    #puede ser que al ser multiplo de 10 ya no queden elementos en la pagina siguiente. Devolvemos lista vacia
                    page_objects=[]
                lista=[i for i in page_objects]
                #return JsonResponse(serializers.serialize('json',lista, use_natural_foreign_keys=True, safe=False)) esta opcion no funcionaba pusieramos en el codigo javascript que recibiamos json como si no
                print HttpResponse(serializers.serialize('json',lista, use_natural_foreign_keys=True))
                return HttpResponse(serializers.serialize('json',lista, use_natural_foreign_keys=True))

def partidas_entre_fechas(request):
    if request.is_ajax():
        if request.method=="GET":
            print request.GET
            lista_partidas=[]
            fecha_inicio=formatoFecha(request.GET.get('id_inicio'))
            print fecha_inicio
            fecha_fin=formatoFecha(request.GET.get('id_fin'))
            print fecha_fin

            partidas=list(PartidaRepositorio.objects.filter(fecha__range=[fecha_inicio, fecha_fin]).order_by("fecha").reverse())
            print partidas
            paginator = Paginator(partidas, 2)
            if request.GET.get('page_number'):
                page_number=request.GET.get('page_number')
                page_objects = paginator.page(page_number).object_list
                print "entremos con pagenumber"
            else:
                page_objects = paginator.page(1).object_list
                print "entramos sin page number"
            for p in page_objects:
                dic_partida={}
                dic_partida["jugador_negro_nombre"]=p.jugador_negro.nombre
                dic_partida["jugador_negro_id"]=p.jugador_negro.id
                dic_partida["jugador_blanco_nombre"]=p.jugador_blanco.nombre
                dic_partida["jugador_blanco_id"]=p.jugador_blanco.id
                dic_partida["rango_negro"]=p.rango_negro
                dic_partida["rango_blanco"]=p.rango_blanco
                dic_partida["fecha"]=p.fecha
                dic_partida["resultado"]=p.resultado
                dic_partida["partida_id"]=p.id
                lista_partidas.append(dic_partida)
            print lista_partidas
            return JsonResponse(lista_partidas, safe=False)

def rest_perfil(request, username):
    p = get_object_or_404(Perfil, user__username=username)
    dic={}
    dic["username"]=username
    dic["nombre"]=p.user.first_name+" "+p.user.last_name
    dic["rango"]=p.rango
    dic["fecha_nacimiento"]=p.fecha_nacimiento
    dic["imagen_principal"]=p.path_principal
    amigos=[]
    for a in p.amigos.all():
        dic_amigo={}
        dic_amigo['username']=a.user.username
        dic_amigo['nombre']=a.user.first_name+" "+a.user.last_name
        amigos.append(dic_amigo)
    dic["amigos"]=amigos
    return JsonResponse(dic)