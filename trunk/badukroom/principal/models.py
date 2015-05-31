from django.db import models
from django.contrib.auth.models import User

from badukroom.settings import MEDIA_ROOT
import random
import string

#esta es una clase para la serializacion de Jugador nos devuelva el nombre
class JugadorManager(models.Manager):
    def get_by_natural_key(self, nombre, id):
        return self.get(nombre=nombre, id=id)

class Jugador(models.Model):
    objects = JugadorManager() #para la serializacion
    nombre=models.CharField(max_length=50, unique=True)
    es_profesional=models.BooleanField(default=False)
    
    def natural_key(self):
        return (self.nombre, self.id)
  
    def __unicode__(self):
        return self.nombre

class Revisor(models.Model):
    perfil=models.OneToOneField('login.Perfil') #asi evitamos import circulares entre distintas app
    nickname_kgs=models.CharField(max_length=20, unique=True)
    #con oneToOne y unique en nickname se comprueba la unicidad del revisor con nick y perfil
    def __unicode__(self):
        return self.nickname_kgs+" ["+self.perfil.rango+"]"

class Sgf(models.Model):
    fichero = models.FileField(upload_to='sgf')
    path = models.CharField(max_length=70,  blank=True)
    
    def __unicode__(self):
        return self.path
    
    def save(self, *args, **kwargs):
        #cambiamos nombre y path para que se apunte al fichero correcto
        name=self.fichero.name
        nombre=name.split('.')
        nombre[0]=nombre[0]+''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(3)) #add terminacion random
        self.fichero.name=nombre[0]+"."+nombre[1]
        camino_fichero="sgf/"+self.fichero.name
        if self.path == "" or self.path==None:
            self.path = camino_fichero
            super(Sgf, self).save(*args, **kwargs)
        else:
            super(Sgf, self).save(*args, **kwargs)
    
class Partida(models.Model):
    fecha = models.DateField()
    jugador_negro = models.ForeignKey(Jugador, related_name='Jugador_jugador_negro')
    rango_negro = models.CharField(max_length=50)
    jugador_blanco = models.ForeignKey(Jugador, related_name='Jugador_jugador_blanco')
    rango_blanco = models.CharField(max_length=50)
    resultado = models.CharField(max_length=50)
    fichero = models.FileField(upload_to='partida')
    path = models.CharField(max_length=70,  blank=True)
    es_profesional=models.BooleanField(default=False)
    #revisor=models.ForeignKey(Revisor, blank=True, null=True) #asignamos revisor y sera considerada partida revisada
    sgf_size=models.IntegerField(default=0)
    class Meta:
        unique_together=('jugador_negro', 'jugador_blanco','fecha', 'sgf_size')
    
    def __unicode__(self):
    #pass
        return self.jugador_blanco.__unicode__()+" - "+self.jugador_negro.__unicode__()+" ["+unicode(self.fecha)+"]"+" "+self.path

    def save(self, *args, **kwargs):
        #Comrpobamos si es profesional
        profesional=["1p", "2p", "3p", "4p", "5p", "6p", "7p", "8p", "9p", "1P", "2P", "3P", "4P", "5P", "6P", "7P", "8P", "9P"]
        if self.rango_blanco in profesional: 
            self.es_profesional=True
            self.jugador_blanco.es_profesional=True
            self.jugador_blanco.save()
        if self.rango_negro in profesional:
            self.es_profesional=True
            self.jugador_negro.es_profesional=True
            self.jugador_negro.save()
        #actualizamos el size con el del fichero para diferenciar entre una partida revisada y otra que no
        self.sgf_size=self.fichero.size
        #cambiamos nombre y path para que se apunte al fichero correcto
        name=self.fichero.name
        nombre=name.split('.')
        nombre[0]=nombre[0]+''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(8)) #add terminacion random
        #self.fichero.name=nombre[0]+"."+nombre[1]
        self.fichero.name=nombre[0]+".sgf"
        camino_fichero="partida/"+self.fichero.name
        if self.path == "" or self.path==None:
            self.path = camino_fichero
            super(Partida, self).save(*args, **kwargs)
        else:
            super(Partida, self).save(*args, **kwargs)

class PartidaRevisada(models.Model):
    fecha = models.DateField()
    jugador_negro = models.CharField(max_length=100)
    rango_negro = models.CharField(max_length=50)
    jugador_blanco = models.CharField(max_length=100)
    rango_blanco = models.CharField(max_length=50)
    resultado = models.CharField(max_length=50)
    fichero = models.FileField(upload_to='revision')
    path = models.CharField(max_length=70,  blank=True)
    revisor=models.ForeignKey(Revisor, blank=True, null=True) #asignamos revisor y sera considerada partida revisada
    sgf_size=models.IntegerField(default=0)
    
    class Meta:
        unique_together=('jugador_negro', 'jugador_blanco','fecha', 'sgf_size')
    
    def __unicode__(self):
        return self.jugador_blanco+" - "+self.jugador_negro+" ["+unicode(self.fecha)+"]"+" "+self.path
    
    def save(self, *args, **kwargs):
        #actualizamos el size con el del fichero para diferenciar entre una partida revisada y otra que no
        self.sgf_size=self.fichero.size
        #cambiamos nombre y path para que se apunte al fichero correcto
        name=self.fichero.name
        nombre=name.split('.')
        nombre[0]=nombre[0]+''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(3)) #add terminacion random
        self.fichero.name=nombre[0]+"."+nombre[1]
        camino_fichero="revision/"+self.fichero.name
        print camino_fichero
        if self.path == "" or self.path==None:
            self.path = camino_fichero
            super(PartidaRevisada, self).save(*args, **kwargs)
        else:
            super(PartidaRevisada, self).save(*args, **kwargs)