from django.db import models
from django.contrib.auth.models import User

from badukroom.settings import MEDIA_ROOT
import random
import string
#from django.core.files.storage import FileSystemStorage

#my_store = FileSystemStorage(location='/static/sgf')

#user and pass is 'tfg' for admin

# Create your models here.

#PROBLEMA A RESOLVER, SE PUEDE GUARDAR VARIAS VECES EL MISMO JUGADOR
# ESTADO: NO RESUELTO

#esta es una clase para la serializacion de Jugador nos devuelva el nombre
class JugadorManager(models.Manager):
    def get_by_natural_key(self, nombre, id):
        return self.get(nombre=nombre, id=id)

class Jugador(models.Model):
    objects = JugadorManager() #para la serializacion
    #primary_key=True
    nombre=models.CharField(max_length=50, unique=True)
    
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

class Partida(models.Model):
    fecha = models.DateField()
    jugador_negro = models.ForeignKey(Jugador, related_name='Jugador_jugador_negro')
    rango_negro = models.CharField(max_length=50)
    jugador_blanco = models.ForeignKey(Jugador, related_name='Jugador_jugador_blanco')
    rango_blanco = models.CharField(max_length=50)
    resultado = models.CharField(max_length=50)
    fichero = models.FileField(upload_to=MEDIA_ROOT+'sgf') #RESOLVER Al add dos ficheros con el mismo nombre el segundo se guarda con un nombre al que se add un sufijo y no coincidira con el del path
    #path = models.CharField(max_length=70, default=fichero.name,  blank=True) #fichero.name devuelve la ruta relativa del fichero: sgf/nombre_fichero, que mostraremos en los templates.
    path = models.CharField(max_length=70,  blank=True)
    revisor=models.ForeignKey(Revisor, blank=True, null=True) #asignamos revisor y sera considerada partida revisada
    sgf_size=models.IntegerField(default=0)
    class Meta:
        unique_together=('jugador_negro', 'jugador_blanco','fecha', 'sgf_size')
    
    def __unicode__(self):
    #pass
        return self.jugador_blanco.__unicode__()+" - "+self.jugador_negro.__unicode__()+" ["+unicode(self.fecha)+"]"+" "+self.path

    def save(self, *args, **kwargs):
        print "En el metodo save() vemos el path: "+self.path
        print self.fichero.size
        #actualizamos el size con el del fichero para diferenciar entre una partida revisada y otra que no
        self.sgf_size=self.fichero.size
        #cambiamos nombre y path para que se apunte al fichero correcto
        print "nombre del fichero: "+self.fichero.name
        name=self.fichero.name
        nombre=name.split('.')
        nombre[0]=nombre[0]+''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(3)) #add terminacion random
        self.fichero.name=nombre[0]+"."+nombre[1]
        print "nombre del fichero: "+self.fichero.name
        camino_fichero="sgf/"+self.fichero.name
        print camino_fichero
        if self.path == "" or self.path==None:
            print "modificamos el path"
            self.path = camino_fichero
            super(Partida, self).save(*args, **kwargs)
        else:
            super(Partida, self).save(*args, **kwargs)
        
        """
        if self.path == "" or self.path==None:
            print "modificamos el path"
            self.path = 'sgf/'+self.fichero.name.__str__() #Sobreescribimos el save para que actualice el path con el nombre del fichero
            super(Partida, self).save(*args, **kwargs)
        else:
            super(Partida, self).save(*args, **kwargs)
        """
class PartidaRepositorio(Partida):
    es_profesional=models.BooleanField(default=False)