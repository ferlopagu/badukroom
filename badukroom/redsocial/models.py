from django.db import models
from login.models import Perfil
from principal.models import Partida
from badukroom.settings import MEDIA_ROOT 
from pip.cmdoptions import editable
from django.template.defaultfilters import default
# Create your models here.



class Comentario(models.Model):
    fecha=models.DateTimeField()
    perfil=models.ForeignKey(Perfil)
    texto=models.CharField(max_length=2000)
    fichero=models.FileField(upload_to=MEDIA_ROOT+'sgf', blank=True)
    #respuestas=models.ManyToManyField(Respuesta, blank=True)
    
    def __unicode__(self):
        return self.perfil.user.username+" "+self.texto

class Respuesta(models.Model):
    perfil=models.ForeignKey(Perfil)
    comentario=models.ForeignKey(Comentario)
    fecha=models.DateTimeField()
    texto=models.CharField(max_length=2000)
    fichero=models.FileField(upload_to=MEDIA_ROOT+'sgf', blank=True)


class PeticionAmistad(models.Model):
    sender=models.ForeignKey(Perfil, related_name='sender')
    receiver=models.ForeignKey(Perfil, related_name='receiver')
    es_aceptada=models.BooleanField(default=False, editable=True)
    es_rechazada=models.BooleanField(default=False, editable=True)
