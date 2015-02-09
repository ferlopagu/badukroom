from django.db import models
from login.models import Perfil
from principal.models import Partida
from badukroom.settings import MEDIA_ROOT 
from pip.cmdoptions import editable
from django.template.defaultfilters import default
# Create your models here.


class PeticionAmistad(models.Model):
    emisor=models.ForeignKey(Perfil, related_name='sender')
    receptor=models.ForeignKey(Perfil, related_name='receiver')
    es_aceptada=models.BooleanField(default=False, editable=True)
    es_rechazada=models.BooleanField(default=False, editable=True)

class Notificacion(models.Model):
    receptor=models.ForeignKey(Perfil)
    mensaje=models.CharField(max_length=300)

class Grupo(models.Model):
    titulo=models.CharField(max_length=300)
    descripcion=models.TextField(max_length=600)
    miembros=models.ManyToManyField(Perfil)
    
    def __unicode__(self):
        return self.titulo

class Comentario(models.Model):
    fecha=models.DateTimeField()
    perfil=models.ForeignKey(Perfil)
    texto=models.CharField(max_length=2000)
    #fichero=models.FileField(upload_to=MEDIA_ROOT+'sgf')
    partida=models.ForeignKey(Partida, null=True, blank=True)
    grupo=models.ForeignKey(Grupo, null=True, blank=True)
    #respuestas=models.ManyToManyField(Respuesta, blank=True)
    
    def __unicode__(self):
        return self.perfil.user.username+" "+self.texto

class Respuesta(models.Model):
    perfil=models.ForeignKey(Perfil)
    comentario=models.ForeignKey(Comentario)
    fecha=models.DateTimeField()
    texto=models.CharField(max_length=2000)
    fichero=models.FileField(upload_to=MEDIA_ROOT+'sgf', blank=True)