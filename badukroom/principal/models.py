from django.db import models
from django.contrib.auth.models import User
from badukroom.settings import MEDIA_ROOT
#from django.core.files.storage import FileSystemStorage

#my_store = FileSystemStorage(location='/static/sgf')

#user and pass is 'tfg' for admin

# Create your models here.

#PROBLEMA A RESOLVER, SE PUEDE GUARDAR VARIAS VECES EL MISMO JUGADOR
# ESTADO: NO RESUELTO
class Jugador(models.Model):
    nombre=models.CharField(max_length=50, primary_key=True)
        
    def __unicode__(self):
        return self.nombre

class Partida(models.Model):
    fecha = models.DateField()
    jugador_negro = models.ForeignKey(Jugador, related_name='Jugador_jugador_negro')
    jugador_blanco = models.ForeignKey(Jugador, related_name='Jugador_jugador_blanco')
    resultado = models.CharField(max_length=50)
    fichero = models.FileField(upload_to=MEDIA_ROOT+'sgf') #RESOLVER Al add dos ficheros con el mismo nombre el segundo se guarda con un nombre al que se add un sufijo y no coincidira con el del path
    #path = models.CharField(max_length=70, default=fichero.name,  blank=True) #fichero.name devuelve la ruta relativa del fichero: sgf/nombre_fichero, que mostraremos en los templates.
    path = models.CharField(max_length=70, default='sgf/'+fichero.name.__str__(),  blank=True)
    class Meta:
        unique_together=('jugador_negro', 'jugador_blanco','fecha')
    
    def __unicode__(self):
    #pass
        return self.jugador_blanco.__unicode__()+" - "+self.jugador_negro.__unicode__()+" ["+unicode(self.fecha)+"]"+" "+self.path

    def save(self, *args, **kwargs):
        self.path = 'sgf/'+self.fichero.name.__str__() #Sobreescribimos el save para que actualice el path con el nombre del fichero
        super(Partida, self).save(*args, **kwargs)