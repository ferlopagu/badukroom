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
from principal.metodosAux import informacion_partida2, estamos_en_grupo, formatoFecha
from badukroom.settings import BASE_DIR
from principal.models import Partida, Jugador, Revisor, Sgf, PartidaRevisada
from django.http import HttpResponse, HttpResponseBadRequest
from django.core.paginator import Paginator, InvalidPage
from django.core import serializers
from .recomendacion import perfiles_amigos, topMatches_amigos_comun, topMatches_gustos
from redsocial.recomendacion import perfiles_gustos
from login.forms import PerfilForm,  UserForm2
from django.contrib.auth.forms import SetPasswordForm
from django.contrib import messages
# Create your views here.
   
@login_required(login_url='/login')
def perfil(request, username):
    p = get_object_or_404(Perfil, user__username=username) #perfil visitado
    comentarios_list=list(Comentario.objects.filter(perfil=p, grupo=None).order_by('fecha').reverse())
    paginator=Paginator(comentarios_list,5)
    comentarios=paginator.page(1).object_list
    yo = get_object_or_404(Perfil, user__username=request.user.username) #mi perfil
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
            elif PeticionAmistad.objects.filter(emisor=p, receptor=usuario_logueado):
                peticion_recibida=True
            else:
                print 'ni son amigos ni le envio la peticion'
    """ FIN comprobamos si el perfil que visualizamos somos nosotros, es un amigo o desconocido """                       
    diccionario_amigos={"es_amigo":es_amigo, 'peticion_enviada':peticion_enviada, 'peticion_recibida':peticion_recibida}
    lista_dic_amigo=[]
    lista_dic_amigo.append(diccionario_amigos) #devolvemos lista con diccionario unico donde especifica si es amigo o no el perfil que visitamos
    
    amigos=p.amigos.all()
    grupos=list(Grupo.objects.filter(miembros__user__username=p.user.username))
    
    formulario_respuesta=ComentarioForm() #formulario para responder a los comentarios
    context = {'comentarios': comentarios, 'formulario_respuesta':formulario_respuesta,'lista_dic_amigo':lista_dic_amigo, 'perfil':p, 'amigos':amigos, 'grupos':grupos, 'somos_nosotros':somos_nosotros, 'perfil_visible':p.visible_perfil, 'es_amigo':diccionario_amigos["es_amigo"]}
    
    if somos_nosotros==True: #somos nosotros luego add formulario para actualizar estado
        formulario=ComentarioForm()
        context['formulario']=formulario
    print 'somos_nosotros: '+str(somos_nosotros)+'\nperfil_visible: '+str(yo.visible_perfil)+'\nes_amigo: '+str(diccionario_amigos["es_amigo"])
    
    return render_to_response('perfil.html',context,context_instance=RequestContext(request))

@login_required(login_url='/login')
def perfil_ajax(request, username):
    p = get_object_or_404(Perfil, user__username=username) 
    comentarios_list=list(Comentario.objects.filter(perfil=p, grupo=None).order_by('fecha').reverse())
    paginator=Paginator(comentarios_list,5)
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
                        dic_respuesta={"texto":r.texto,"fecha":r.fecha, "imagen_perfil":r.perfil.path_principal, "username":r.perfil.user.username, "nombre":r.perfil.user.first_name}
                        if r.partida != None:
                            dic_respuesta["partida"]=r.partida.path
                        else:
                            dic_respuesta["partida"]=""
                        lista_respuestas.append(dic_respuesta)
                    dic_comentario["respuestas"]=lista_respuestas
                    lista_comentarios.append(dic_comentario)
                print JsonResponse(lista_comentarios, safe=False)
                return JsonResponse(lista_comentarios, safe=False)

@login_required(login_url='/login')
def comentarios_scroll(request):
    comentarios=list(Comentario.objects.values())
    paginator = Paginator(comentarios, 15)
    if request.method == 'GET':
        if request.is_ajax():
            if request.GET.get('page_number'):
                page_number = request.GET.get('page_number');
                try:
                    page_objects = paginator.page(page_number).object_list
                except InvalidPage:
                    return HttpResponseBadRequest(mimetype="json")
                lista=[i for i in page_objects]
                resp=lista
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
    print "Soy redirigido"
    username=request.user.username
    p = get_object_or_404(Perfil, user__username=username)
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
    formulario=ComentarioForm()
    formulario_respuesta=ComentarioForm()
    context = {'comentarios': comentarios,'formulario':formulario, 'perfil':p, 'formulario_respuesta':formulario_respuesta }
    return render_to_response('home.html',context,context_instance=RequestContext(request))

@login_required(login_url='/login')
def home_ajax(request): #No se para que recojo la variable username si luego la redefino
    username=request.user.username
    p = get_object_or_404(Perfil, user__username=username)
    comentarios_list=list(Comentario.objects.filter( (Q(perfil=p) | Q(perfil__in=p.amigos.all(), grupo=None)) | Q(grupo__miembros=p)).distinct().order_by('fecha').reverse())
    paginator=Paginator(comentarios_list,5)
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
                        dic_respuesta={"texto":r.texto,"fecha":r.fecha, "imagen_perfil":r.perfil.path_principal, "username":r.perfil.user.username, "nombre":r.perfil.user.first_name}
                        if r.partida != None:
                            dic_respuesta["partida"]=r.partida.path
                        else:
                            dic_respuesta["partida"]=""
                        lista_respuestas.append(dic_respuesta)
                    dic_comentario["respuestas"]=lista_respuestas
                    lista_comentarios.append(dic_comentario)
                return JsonResponse(lista_comentarios, safe=False)

@login_required(login_url='/login')
def crea_comentario(request):
    if request.is_ajax():
        if 'fichero' in request.FILES: #comprobamos que tenga fichero
            form = ComentarioForm(request.POST, request.FILES)
            if form.is_valid():
                fecha=datetime.now()
                perfil=Perfil.objects.get(user=request.user)
                partida = Sgf(fichero=request.FILES['fichero'])
                if partida.extension() == ".sgf":
                    partida.save()
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
                    comentarios=list(Comentario.objects.values())
                    return JsonResponse(comentarios, safe=False)
                else:
                    print "El fichero subido no tiene la extension correspondiente"
                    dic={"error": "No ha sido posible publicar el comentario. El fichero no tiene extensión .sgf."}
                    return JsonResponse(dic)
            else:
                print "el formulario no es valido"
                dic={"error": "No ha sido posible publicar el comentario. Recuerde rellenar el campo de texto al menos."}
                return JsonResponse(dic)
        else:#no adjuntamos fichero
            form = ComentarioForm(request.POST)
            if form.is_valid():
                fecha=datetime.now()
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
                comentarios=list(Comentario.objects.values())
                return JsonResponse(comentarios, safe=False)
            else:
                print "no se contenia fichero pero el formulario no era valido"
                dic={"error": "No ha sido posible publicar el comentario. Recuerde rellenar el campo de texto al menos."}
                return JsonResponse(dic)
    else:
        print "ENTRAMOS EN ELSE AL NO SER AJAX"
        return HttpResponseRedirect(request.META['HTTP_REFERER'])

@login_required(login_url='/login')
def responder(request):
    if request.is_ajax():
        id_comentario=int(request.POST["id_comentario"])
        if 'fichero' in request.FILES: #comprobamos que tenga fichero
            form = ComentarioForm(request.POST, request.FILES)
            if form.is_valid():
                fecha=datetime.now()
                perfil=Perfil.objects.get(user=request.user)
                partida = Sgf(fichero=request.FILES['fichero'])
                if partida.extension() == ".sgf":
                    partida.save()
                    partida=partida
                    texto=form.cleaned_data['texto']
                    comentario=Comentario.objects.get(id=id_comentario)
                    respuesta=Respuesta(fecha=fecha, perfil=perfil, texto=texto, partida=partida, comentario=comentario)
                    respuesta.save()
                    comentarios=list(Comentario.objects.values())
                    return JsonResponse(comentarios, safe=False)
                else:
                    print "El fichero subido no tiene la extension .sgf"
                    dic={"error": "No ha sido posible publicar el comentario. El fichero no tiene extensión .sgf."}
                    return JsonResponse(dic)
            else:
                dic={"error": "No ha sido posible publicar su respuesta. Recuerde rellenar el campo de texto al menos."}
                return JsonResponse(dic)
                print "el formulario no es valido"
        else:#no adjuntamos fichero
            form = ComentarioForm(request.POST)
            if form.is_valid():
                fecha=datetime.now()
                perfil=Perfil.objects.get(user=request.user)
                texto=form.cleaned_data['texto']
                comentario=Comentario.objects.get(id=id_comentario)
                respuesta=Respuesta(fecha=fecha, perfil=perfil, texto=texto, comentario=comentario)
                respuesta.save()
                comentarios=list(Comentario.objects.values())
                return JsonResponse(comentarios, safe=False)
            else:
                dic={"error": "No ha sido posible publicar su respuesta. Recuerde rellenar el campo de texto al menos."}
                return JsonResponse(dic)
                print "no se contenia fichero pero el formulario no era valido"
    else:
        print "ENTRAMOS EN ELSE AL NO SER AJAX"
        return HttpResponseRedirect(request.META['HTTP_REFERER'])

@login_required(login_url='/login')
def buscador(request):
    if request.is_ajax():
        if request.method=='GET':
            cadena=request.GET['texto']
            #usaremos irregex para diferenciar entre minusculas y mayusculas  
            if cadena!="":
                lista_perfiles=list(Perfil.objects.values('user__first_name', 'user__last_name', 'user__username','path_principal').filter(Q(user__first_name__iregex=cadena) | Q(user__last_name__iregex=cadena))) #cambiar username por first_name o last_nameprint lista_perfiles
                lista_grup=list(Grupo.objects.values('id', 'titulo').filter(titulo__iregex=cadena))
                lista_res=[]
                lista_res.append(lista_perfiles)
                lista_res.append(lista_grup)
                return JsonResponse(lista_res, safe=False)
            else:
                lista_perfiles=[]
                return JsonResponse(lista_perfiles, safe=False)
        else:
            render("Hubo un problema en su peticion")
    else:
        lista_grup=[]
        lista_perfiles=[]
        if request.method=='POST':
            cadena=request.POST['buscar_texto']
            #usaremos irregex para diferenciar entre minusculas y mayusculas
            if cadena!="":
                lista_perfiles=list(Perfil.objects.filter(Q(user__first_name__iregex=cadena) | Q(user__last_name__iregex=cadena))) #cambiar username por first_name o last_nameprint lista_perfiles
                lista_grup=list(Grupo.objects.filter(titulo__iregex=cadena))
            context={'lista_perfiles':lista_perfiles, 'lista_grupos':lista_grup}
            return render_to_response('busqueda.html', context, context_instance=RequestContext(request))
        #return HttpResponseRedirect(request.META['HTTP_REFERER']) #Asi recargariamos la página

@login_required(login_url='/login')
def agregar_ajax(request):
    if request.is_ajax():
        if request.method=='POST':
            username_receptor=request.POST['perfil_para_agregar']
            print "Perfil para agregar: "+username_receptor
            emisor=get_object_or_404(Perfil, user__username=request.user.username)
            receptor=get_object_or_404(Perfil, user__username=username_receptor)
            es_aceptada=False
            es_rechazada=False
            peticion=PeticionAmistad(emisor=emisor, receptor=receptor, es_aceptada=es_aceptada, es_rechazada=es_rechazada)
            peticion.save()
            return HttpResponse("Peticion de amistad enviada con éxito")
    else:
        print "fue un fracaso la peticion ajax"

@login_required(login_url='/login')
def eliminar_ajax(request):
    if request.is_ajax():
        if request.method=='GET':
            username_amigo=request.GET['perfil_para_eliminar']
            yo=get_object_or_404(Perfil, user__username=request.user.username)
            amigo=get_object_or_404(Perfil, user__username=username_amigo)
            yo.amigos.remove(amigo)
            yo.save()
            return HttpResponse("Eliminado con éxito")
    else:
        return HttpResponse("Problema con peticion ajax")

@login_required(login_url='/login')
def contar_notificaciones(request):
    if request.is_ajax():
        if request.method=='GET':
            recuento_peticiones = PeticionAmistad.objects.filter(receptor__user__username=request.user.username).count()
            recuento_notificaciones=Notificacion.objects.filter(receptor__user__username=request.user.username).count()
            recuento_peticiones_revision=PeticionRevision.objects.filter(receptor__user__username=request.user.username).count()
            recuento=recuento_notificaciones+recuento_peticiones+recuento_peticiones_revision
            return HttpResponse(recuento)
    else:
        print "no es peticion ajax o GET"

@login_required(login_url='/login')
def ver_notificaciones(request):
    lista_peticiones=list(PeticionAmistad.objects.filter(receptor__user__username=request.user.username))
    lista_notificaciones=list(Notificacion.objects.filter(receptor__user__username=request.user.username))
    lista_peticiones_revision=list(PeticionRevision.objects.filter(receptor__user__username=request.user.username))
    form=SgfForm()
    context={'lista_peticiones': lista_peticiones, 'lista_notificaciones': lista_notificaciones, 'form':form, 'lista_peticiones_revision': lista_peticiones_revision}
    return render_to_response('notificaciones.html',context,context_instance=RequestContext(request))

@login_required(login_url='/login')
def aceptar_peticion(request):
    if request.is_ajax():
        if request.method=='POST':
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

@login_required(login_url='/login')
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

@login_required(login_url='/login')
def limpiar_notificaciones(request):
    if request.is_ajax():
        if request.method=='GET':
            boton = request.GET['boton']
            receptor= get_object_or_404(Perfil, user__username=request.user.username)
            if boton=='limpiar_notificaciones':
                Notificacion.objects.filter(receptor=receptor).delete()
            elif boton=='limpiar_peticiones':
                PeticionAmistad.objects.filter(receptor=receptor).delete()
            elif boton=='limpiar_revisiones':
                PeticionRevision.objects.filter(receptor=receptor).delete()
            return HttpResponse("Se borraron correctamente.")
    else:
        return HttpResponse('Error en la peticion Ajax')

@login_required(login_url='/login')          
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

@login_required(login_url='/login')
def lista_grupos(request):
    p=get_object_or_404(Perfil, user__username=request.user.username)
    grupos=list(Grupo.objects.values('titulo','descripcion','pk').filter(miembros__user__username=p.user.username))
    form=GrupoForm()
    context = {'lista_grupos': grupos,'form':form}
    return render_to_response('lista_grupos.html',context,context_instance=RequestContext(request))

@login_required(login_url='/login')
def lista_todos_grupos(request):
    grupos=list(Grupo.objects.values('titulo','descripcion','pk').all().order_by("titulo"))
    form=GrupoForm()
    context = {'lista_grupos': grupos,'form':form}
    return render_to_response('lista_grupos_total.html',context,context_instance=RequestContext(request))

@login_required(login_url='/login')
def amigos(request):
    p=get_object_or_404(Perfil, user__username=request.user.username)
    amigos=list(p.amigos.all())
    """ add perfiles recomendados """
    diccionario_amigos=perfiles_amigos()
    lista_recomendacion_comun=topMatches_amigos_comun(diccionario_amigos, p)
    print lista_recomendacion_comun
    recomendacion_comun=True
    print lista_recomendacion_comun[0][0]
    if lista_recomendacion_comun[0][0]==0:
        recomendacion_comun=False
    diccionario_gustos=perfiles_gustos()
    lista_recomendacion_gustos=topMatches_gustos(diccionario_gustos, p)
    recomendacion_gustos=True
    if lista_recomendacion_gustos[0][0]==0:
        recomendacion_gustos=False
    print lista_recomendacion_gustos
    """ fin perfiles recomendados"""
    context = {'lista_amigos': amigos, 'lista_recomendacion_comun': lista_recomendacion_comun, 'lista_recomendacion_gustos': lista_recomendacion_gustos, 'rec_gustos':recomendacion_gustos, 'rec_comun':recomendacion_comun}
    return render_to_response('amigos.html', context, context_instance=RequestContext(request))

@login_required(login_url='/login')
def partidas(request):
    """ Obtenemos partidas repositorio profesionales"""
    partidas_p=list(Partida.objects.filter(es_profesional=True).order_by('fecha').reverse())
    paginator_p = Paginator(partidas_p, 10)
    lista_partidas_profesionales=paginator_p.page(1).object_list
    """ Obtenemos partidas repositorio amateur """
    partidas_a=list(Partida.objects.filter(es_profesional=False).order_by('fecha').reverse())
    paginator_a = Paginator(partidas_a, 10)
    lista_partidas_amateur=paginator_a.page(1).object_list 
    """ Devolvemos diccionario con todos los jugadores del sistema nombres de jugadores"""
    dic_jugadores_p={}
    dic_jugadores_a={}
    abecedario= ["A", "B", "C", "D", "E", "F", "G","H","I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]
    for letra in abecedario:
        lista_p=[]
        lista_a=[]
        for j in Jugador.objects.filter(nombre__startswith=letra).order_by("nombre"):
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
 
@login_required(login_url='/login')   
def partidas_ajax(request):
    partidas=list(Partida.objects.all().order_by('fecha').reverse())
    paginator = Paginator(partidas, 10)
    if request.is_ajax():
        if request.method=="GET":
            if request.GET.get('page_number'):
                page_number = request.GET.get('page_number');
                try:
                    page_objects = paginator.page(page_number).object_list
                except InvalidPage:
                    page_objects=[]
                lista=[i for i in page_objects]
                return HttpResponse(serializers.serialize('json',lista, use_natural_foreign_keys=True))

@login_required(login_url='/login')          
def partidas_jugador(request, id):
    partidas=list(Partida.objects.filter(Q(jugador_negro__id=id) | Q(jugador_blanco__id=id)))
    paginator= Paginator(partidas, 2)
    jugador=Jugador.objects.get(id=id)
    if request.is_ajax():
        if request.method=="GET":
            page_number=request.GET.get("page_number");
            try:
                page_objects = paginator.page(page_number).object_list
            except InvalidPage:
                page_objects=[]
            lista_partidas=[]
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
            return JsonResponse(lista_partidas, safe=False)          
    else:
        lista=paginator.page(1).object_list
        perfil=Perfil.objects.get(user__username=request.user.username)
        me_gusta=False
        if jugador in perfil.jugadores_favoritos.all():
            print "El jugador me gusta"
            me_gusta=True
        context={'partidas': lista, 'jugador':jugador.nombre, 'me_gusta':me_gusta}
        return render_to_response('jugador.html', context, context_instance=RequestContext(request))

@login_required(login_url='/login')
def revisiones(request):
    partidas=list(PartidaRevisada.objects.all().order_by('fecha').reverse())
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
                print p
                dic_partida={}
                dic_partida["revisor_nickname"]=p.revisor.nickname_kgs
                dic_partida["revisor_rango"]=p.revisor.perfil.rango
                dic_partida["jugador_negro_nombre"]=p.jugador_negro
                dic_partida["jugador_blanco_nombre"]=p.jugador_blanco
                dic_partida["rango_negro"]=p.rango_negro
                dic_partida["rango_blanco"]=p.rango_blanco
                dic_partida["fecha"]=p.fecha
                dic_partida["resultado"]=p.resultado
                dic_partida["partida_id"]=p.id
                lista_partidas.append(dic_partida)
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
        context={'partidas_revisadas':lista, 'form':form, 'revisores': revisores, 'soy_revisor':soy_revisor}
        return render(request,name, context)

@login_required(login_url='/login')
def partidas_by_revisor(request, nickname_kgs):
    partidas=list(PartidaRevisada.objects.filter(revisor__nickname_kgs=nickname_kgs).order_by('fecha').reverse())
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
                dic_partida["jugador_negro_nombre"]=p.jugador_negro
                dic_partida["jugador_blanco_nombre"]=p.jugador_blanco
                dic_partida["rango_negro"]=p.rango_negro
                dic_partida["rango_blanco"]=p.rango_blanco
                dic_partida["fecha"]=p.fecha
                dic_partida["resultado"]=p.resultado
                dic_partida["partida_id"]=p.id
                lista_partidas.append(dic_partida)
            print lista_partidas
            return JsonResponse(lista_partidas, safe=False)

@login_required(login_url='/login')
def crear_grupo(request):
    print "ENTRO EN CREAR GRUPO"
    if request.method=="POST":
        if 'foto_portada' in request.FILES: #comprobamos que tenga fichero
            form = GrupoForm(request.POST, request.FILES)
            print form
            if form.is_valid():
                titulo=form.cleaned_data['titulo']
                descripcion=form.cleaned_data['descripcion']
                foto_portada=form.cleaned_data['foto_portada']
                grupo, created=Grupo.objects.get_or_create(titulo=titulo, descripcion=descripcion, foto_portada=foto_portada)
                perfil=Perfil.objects.get(user__username=request.user.username)
                grupo.miembros.add(perfil)
                grupo.save()
                print "EL GRUPO CON FOTO HA SIDO SALVADO"
                return HttpResponseRedirect(request.META['HTTP_REFERER'])
            else:
                print "el fichero con imagen no es valido"
        else:
            form = GrupoForm(request.POST)
            if form.is_valid():
                titulo=form.cleaned_data['titulo']
                descripcion=form.cleaned_data['descripcion']
                grupo, created=Grupo.objects.get_or_create(titulo=titulo, descripcion=descripcion)
                perfil=Perfil.objects.get(user__username=request.user.username)
                grupo.miembros.add(perfil)
                grupo.save()
                return HttpResponseRedirect(request.META['HTTP_REFERER'])
            else:
                print "el formulario sin imagen no es valido"
    else:
        print "el metodo no es POST"

#Sistema de revisiones de partidas
@login_required(login_url='/login')
def enviar_partida_revisar(request):
    form = EnvioForm(request.POST, request.FILES)
    if form.is_valid():
        p=Perfil.objects.get(user__username=request.user.username)
        revisor=Revisor.objects.get(id=request.POST['revisor'])
        if not PeticionRevision.objects.filter(receptor=revisor.perfil, emisor=p):
            fichero = form.clean_fichero()
            partida = Sgf(fichero=request.FILES['fichero'])
            if partida.extension() == ".sgf":
                partida.save()
                """ Fin crear la partida """
                """Mandamos las notificaciones"""
                mensaje_a_revisor="Tienes una nueva partida para revisar, puedes descargarla aqui: <a href='/media/"+partida.path+"'>Descargar</a>."
                peticion=PeticionRevision(receptor=revisor.perfil, emisor=p, mensaje=mensaje_a_revisor, partida_id=partida.id)
                peticion.save()
                notificacion2=Notificacion(receptor=p, mensaje="Tu partida ha sido asignada con éxito, te rogamos esperes unos días antes de volver a enviarla a otro revisor.")
                notificacion2.save()
                return HttpResponseRedirect(request.META['HTTP_REFERER']) #recargamos la página
            else:
                messages.add_message(request, messages.INFO, "No se ha podido subir la partida. Puede que no la haya seleccionado correctamente.")
                return HttpResponseRedirect(request.META['HTTP_REFERER'])
        else:
            return ver_notificaciones(request)
    else:
        #dic={"error": "No ha sido posible subir la partida. Puede que no la ha seleccionado correctamente."}
        #return JsonResponse(dic)
        messages.add_message(request, messages.INFO, "No se ha podido subir la partida. Puede que no la haya seleccionado correctamente.")
        return HttpResponseRedirect(request.META['HTTP_REFERER'])
        

@login_required(login_url='/login')
def aceptar_partida_revisar(request, username):
    #aqui ya mandamos la partida suponemos que acepta si la revisa y sino la va a revisar rechazara cuando lea la notificacion
    revisor=Revisor.objects.get(perfil__user__username=request.user.username)
    form = SgfForm(request.POST, request.FILES)
    if form.is_valid():
        """ Estamos leyendo la partida y sacando la informacion util para crearla"""
        path_fichero=BASE_DIR+"/static/sgf/"+request.FILES['fichero'].__str__()
        lineas=request.FILES['fichero'].chunks()
        diccionario_informacion=informacion_partida2(lineas, path_fichero) 
        partida = PartidaRevisada(fecha=diccionario_informacion['fecha'], jugador_negro=diccionario_informacion['black'], 
                          jugador_blanco=diccionario_informacion['blanco'], rango_negro=diccionario_informacion['rango_negro'],rango_blanco=diccionario_informacion['rango_blanco'], resultado=diccionario_informacion['result'], 
                          fichero=request.FILES['fichero'], revisor=revisor)
        if partida.extension() == ".sgf":
            partida.save()
            """ Fin crear la partida """
            """Mandamos las notificaciones"""
            mensaje_a_usuario="La partida ha sido revisada, puedes descargarla aqui: <a href='/media/"+partida.path+"'>Descargar</a>. O visualizarla desde el apartado de Revisiones"
            p=Perfil.objects.get(user__username=username)
            notificacion1=Notificacion(receptor=p, mensaje=mensaje_a_usuario)
            notificacion1.save()
            notificacion2=Notificacion(receptor=revisor.perfil, mensaje="La partida revisada fue almacenada con éxito en el sistema")
            notificacion2.save()
            peticion=PeticionRevision.objects.get(receptor=revisor.perfil, emisor=p)
            #Borramos sgf
            sgf = Sgf.objects.get(id=peticion.partida_id)
            sgf.delete()
            print "borramos SGF"
            #Fin borrar sgf
            peticion.delete()
            return HttpResponseRedirect(request.META['HTTP_REFERER']) #recargamos la página
        else:
            messages.add_message(request, messages.INFO, "No se ha podido subir la partida. Puede que no la haya seleccionado correctamente.")
            return HttpResponseRedirect(request.META['HTTP_REFERER'])
    else:
        print "el formulario no es valido"
        messages.add_message(request, messages.INFO, "No se ha podido subir la partida. Puede que no la haya seleccionado correctamente.")
        return HttpResponseRedirect(request.META['HTTP_REFERER'])

@login_required(login_url='/login')
def rechazar_partida_revisar(request):
    perfil = Perfil.objects.get(user=request.user)
    peticion_rev=PeticionRevision.objects.get(receptor=perfil)
    id_partida=peticion_rev.partida_id 
    partida=get_object_or_404(Sgf, pk=id_partida) #aqui parece estar el fallo
    partida.delete()
    print "borramos la partida"
    emisor_peticion=peticion_rev.emisor
    mensaje="El revisor "+perfil.user.username+" no puede atender tu peticion. Por favor, vuelve a mandar el fichero sgf a otro revisor. Gracias."
    notificacion=Notificacion(receptor=emisor_peticion, mensaje=mensaje)
    notificacion.save()
    print "almacenamos notificacion"
    peticion_rev.delete()
    print "borramos peticion"
    return HttpResponseRedirect(request.META['HTTP_REFERER'])

@login_required(login_url='/login')
def ver_partida(request, partida_id):
    partida=get_object_or_404(Partida, pk=partida_id)
    name="ver_partida.html"
    context={'partida':partida}
    return render(request,name, context)

@login_required(login_url='/login')
def ver_partida_revisada(request, partida_id):
    partida=get_object_or_404(PartidaRevisada, pk=partida_id)
    name="ver_partida.html"
    context={'partida':partida}
    return render(request,name, context)

@login_required(login_url='/login')
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

@login_required(login_url='/login')
def crear_partida_repositorio(request):
    if request.method=='POST':
        form = EnvioForm(request.POST, request.FILES)
        if form.is_valid():
            profesionales=["1p", "2p", "3p", "4p", "5p", "6p", "7p", "8p", "9p"]
            path_fichero=BASE_DIR+"/static/sgf/"+request.FILES['fichero'].__str__()
            lineas=request.FILES['fichero'].chunks()
            diccionario_informacion=informacion_partida2(lineas, path_fichero)
            print diccionario_informacion
            jugador_negro, created = Jugador.objects.get_or_create(nombre=diccionario_informacion['black'])
            jugador_blanco, created = Jugador.objects.get_or_create(nombre=diccionario_informacion['blanco'])
            partida = Partida(fecha=diccionario_informacion['fecha'], jugador_negro=jugador_negro, 
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
            print 'partida salvada con exito'
            return HttpResponseRedirect("partidas")
        else:
            messages.add_message(request, messages.INFO, "No ha sido posible subir la partida al repositorio. Comprueba que ha seleccionado correctamente un fichero .sgf")
            return HttpResponseRedirect(request.META['HTTP_REFERER'])
    else:
        print "no entramos en POST"

@login_required(login_url='/login')
def unirse_revisor(request):
    if request.is_ajax():
        if request.method=='POST':
            print request.POST
            p=Perfil.objects.get(user__username=request.user.username)
            revisor=Revisor(perfil=p, nickname_kgs=request.POST['nick'])
            revisor.save()
            print revisor.__unicode__()
            return HttpResponse("Ha sido un exito")

@login_required(login_url='/login')       
def dejar_revisor(request):
    if request.is_ajax():
        if request.method=='GET':
            p=Perfil.objects.get(user__username=request.user.username)
            revisor=Revisor.objects.get(perfil=p)
            revisor.delete()
            return HttpResponse("Ha sido un exito")

@login_required(login_url='/login')
def fuerza_revisor(request):  
    if request.is_ajax():
        if request.method=="GET":
            page_number = request.GET.get('page_number');
            try:
                rango_revisor=request.GET.get('rango')
                partidas=list(PartidaRevisada.objects.filter(revisor__perfil__rango=rango_revisor).order_by('fecha').reverse())
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
                dic_partida["jugador_negro_nombre"]=p.jugador_negro
                dic_partida["jugador_blanco_nombre"]=p.jugador_blanco
                dic_partida["rango_negro"]=p.rango_negro
                dic_partida["rango_blanco"]=p.rango_blanco
                dic_partida["fecha"]=p.fecha
                dic_partida["resultado"]=p.resultado
                dic_partida["partida_id"]=p.id
                lista_partidas.append(dic_partida)
            print lista_partidas
            return JsonResponse(lista_partidas, safe=False)

@login_required(login_url='/login')
def fuerza_jugador(request):
        if request.is_ajax():
            if request.method=="GET":
                page_number = request.GET.get('page_number');
                try:
                    rango_jugador=request.GET.get('rango')
                    partidas=list(PartidaRevisada.objects.filter(Q(rango_negro=rango_jugador)|Q(rango_blanco=rango_jugador)).order_by('fecha').reverse())
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
                    dic_partida["jugador_negro_nombre"]=p.jugador_negro
                    dic_partida["jugador_blanco_nombre"]=p.jugador_blanco
                    dic_partida["rango_negro"]=p.rango_negro
                    dic_partida["rango_blanco"]=p.rango_blanco
                    dic_partida["fecha"]=p.fecha
                    dic_partida["resultado"]=p.resultado
                    dic_partida["partida_id"]=p.id
                    lista_partidas.append(dic_partida)
                print lista_partidas
                return JsonResponse(lista_partidas, safe=False)

@login_required(login_url='/login')
def recargar_repositorio_ajax(request):
    if request.is_ajax():
        if request.method=="GET":
            if request.GET.get('page_number'):
                if request.GET.get('profesional'):
                    partidas=list(Partida.objects.filter(es_profesional=True).order_by('fecha').reverse())
                    paginator = Paginator(partidas, 10)
                    print "recargamos las profesionales"
                else: #pedimos recargar el amateur
                    partidas=list(Partida.objects.filter(es_profesional=False).order_by('fecha').reverse())
                    paginator = Paginator(partidas, 10)
                    print "recargamos las amateur"
                page_number = request.GET.get('page_number');
                print page_number
                try:
                    page_objects = paginator.page(page_number).object_list
                    print page_objects
                except InvalidPage:
                    page_objects=[]
                lista_partidas=[]
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
                return JsonResponse(lista_partidas, safe=False)

@login_required(login_url='/login')
def partidas_entre_fechas(request):
    if request.is_ajax():
        if request.method=="GET":
            lista_partidas=[]
            fecha_inicio=formatoFecha(request.GET.get('id_inicio'))
            fecha_fin=formatoFecha(request.GET.get('id_fin'))
            partidas=list(Partida.objects.filter(fecha__range=[fecha_inicio, fecha_fin]).order_by("fecha").reverse())
            paginator = Paginator(partidas, 2)
            if request.GET.get('page_number'):
                try:
                    page_number=request.GET.get('page_number')
                    page_objects = paginator.page(page_number).object_list
                except InvalidPage:
                    page_objects=[]
            else:
                page_objects = paginator.page(1).object_list
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

@login_required(login_url='/login')
def unirse_grupo(request):
    if request.is_ajax():
        if request.method=='POST':
            print request.POST
            g = Grupo.objects.get(id=request.POST['grupo_id'])
            p=Perfil.objects.get(user__username=request.user.username)
            g.miembros.add(p)
            g.save()
            return HttpResponse("Ha sido un exito")

@login_required(login_url='/login')
def dejar_grupo(request):
    if request.is_ajax():
        if request.method=='POST':
            print request.POST
            g = Grupo.objects.get(id=request.POST['grupo_id'])
            p=Perfil.objects.get(user__username=request.user.username)
            g.miembros.remove(p)
            g.save()
            if g.miembros.all().count()==0:
                g.delete()
                return JsonResponse({"vacio":True})
            return HttpResponse("Ha sido un exito")

@login_required(login_url='/login')
def configuracion(request): 
    instance_perfil = Perfil.objects.get(user=request.user)
    instance_user = User.objects.get(id=instance_perfil.user.id)
    form_perfil = PerfilForm(request.POST or None,request.FILES or None, instance=instance_perfil)
    form_user=UserForm2(request.POST or None, instance=instance_user)
    #form = PasswordChangeForm(user=request.user, data=request.POST)
    form = SetPasswordForm(user=request.user, data=request.POST)
    if request.method=='POST':
        if form_perfil.is_valid() and form_user.is_valid(): #El usuario actualiza su informacion
            form_perfil.save()
            form_user.save()
            if form.is_valid(): # y tambien actualiza su password
                form.save()
                return HttpResponseRedirect("/")   
            return HttpResponseRedirect("configuracion")       
        if form.is_valid(): #el usuario actualiza solo su password
            print form
            form.save()
            return HttpResponseRedirect("/")
        return HttpResponse('salvado con exito la informacion')
    context={'form_perfil': form_perfil, 'form_user':form_user, 'form': form}
    name='configuracion.html'
    return render(request,name, context)

@login_required(login_url='/login')
def dejar_seguir(request):
    perfil = Perfil.objects.get(user=request.user)
    if request.method=='POST':
        jugador=Jugador.objects.get(id=request.POST["id_jugador"])
        perfil.jugadores_favoritos.remove(jugador)
        perfil.save()
        print "PERFIL ACTUALIZADO"
        return JsonResponse({})

@login_required(login_url='/login')
def seguir_jugador(request):
    perfil = Perfil.objects.get(user=request.user)
    if request.method=='POST':
        jugador=Jugador.objects.get(id=request.POST["id_jugador"])
        perfil.jugadores_favoritos.add(jugador)
        perfil.save()
        print "PERFIL ACTUALIZADO"
        return JsonResponse({})

@login_required(login_url='/login')
def eliminar_cuenta(request):
    print "Entro en eliminar cuenta"
    user = User.objects.get(username=request.user.username)
    user.delete()
    print "PERFIL BORRADO"
    return HttpResponseRedirect("/")