from django.db import models
from login.models import Perfil
from principal.models import Sgf
import random
import string
# Create your models here.


class PeticionAmistad(models.Model):
    emisor=models.ForeignKey(Perfil, related_name='sender')
    receptor=models.ForeignKey(Perfil, related_name='receiver')
    es_aceptada=models.BooleanField(default=False, editable=True)
    es_rechazada=models.BooleanField(default=False, editable=True)

class Notificacion(models.Model):
    receptor=models.ForeignKey(Perfil)
    mensaje=models.CharField(max_length=300)
    revision=models.BooleanField(default=False)


class PeticionRevision(models.Model):
    emisor=models.ForeignKey(Perfil, related_name='sender1')
    receptor=models.ForeignKey(Perfil, related_name='receiver1')
    mensaje=models.CharField(max_length=300)
    partida_id=models.IntegerField() #campo para quedarnos con el id de la partida

class Grupo(models.Model):
    titulo=models.CharField(max_length=300)
    descripcion=models.TextField(max_length=600)
    miembros=models.ManyToManyField(Perfil)
    foto_portada=models.ImageField( blank=True, upload_to='imagenes', default="imagenes/sin_portada.jpg")
    path_portada = models.CharField(max_length=70, default='imagenes/sin_portada.jpg' ,blank=True)
    
    def __unicode__(self):
        return self.titulo
    
    def save(self, *args, **kwargs):
        array=self.foto_portada.name.split("/")
        nombre_portada=array[len(array)-1]
        if self.path_portada != 'imagenes/'+nombre_portada: 
            if self.path_portada == "" or self.path_portada==None or self.foto_portada==None:
                self.path_portada='imagenes/sin_portada.jpg'
            else:
                self.foto_portada.name=''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(3))+nombre_portada #add principio random
                path_portada="imagenes/"+self.foto_portada.name
                self.path_portada=path_portada
        super(Grupo, self).save(*args, **kwargs)
    

class Comentario(models.Model):
    fecha=models.DateTimeField()
    perfil=models.ForeignKey(Perfil)
    texto=models.TextField()
    partida=models.ForeignKey(Sgf, null=True, blank=True)
    grupo=models.ForeignKey(Grupo, null=True, blank=True)
    
    def __unicode__(self):
        return self.perfil.user.username+" "+self.texto

class Respuesta(models.Model):
    perfil=models.ForeignKey(Perfil)
    comentario=models.ForeignKey(Comentario)
    fecha=models.DateTimeField()
    texto=models.CharField(max_length=2000)
    partida=models.ForeignKey(Sgf, null=True, blank=True)
