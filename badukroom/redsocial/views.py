# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.template.context import RequestContext
from redsocial.models import Comentario, Respuesta, PeticionAmistad, Notificacion
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
from principal.metodosAux import informacion_partida, informacion_partida2
from badukroom.settings import BASE_DIR
from principal.models import Partida, Jugador
# Create your views here.
#@login_required(login_url='/login')
def perfil(request, username):
    print request.user
    #return render_to_response('inicio.html', locals())   
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
        print request.POST
        print "request.Files"
        print request.FILES
        form = ComentarioForm(request.POST, request.FILES)
        if form.is_valid():
            print form
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
            jugador_negro=Jugador(nombre=diccionario_informacion['black'])
            jugador_negro.save()
            print 'jugador negro guardado con exito'
            jugador_blanco=Jugador(nombre=diccionario_informacion['blanco'])
            jugador_blanco.save()
            partida = Partida(fecha=diccionario_informacion['fecha'], jugador_negro=jugador_negro, 
                              jugador_blanco=jugador_blanco, resultado=diccionario_informacion['result'], 
                              fichero=request.FILES['fichero'], path=diccionario_informacion['path'])
            partida.save()
            print partida.__unicode__()
            print 'partida salvada con exito'
            """ Fin crear la partida """
            perfil=perfil
            partida=partida
            texto=form.cleaned_data['texto']
            comentario=Comentario(fecha=fecha, perfil=perfil, texto=texto, partida=partida)
            comentario.save()
            print 'comentario guardado con exito'
            comentarios=list(Comentario.objects.values())
            return JsonResponse(comentarios, safe=False)
        else:
            print "el formulario no es valido"
            print request.POST
            print request.FILES
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
    context={'lista_peticiones': lista_peticiones, 'lista_notificaciones': lista_notificaciones}
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
           
