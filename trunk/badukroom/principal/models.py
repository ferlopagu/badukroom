from django.db import models
from django.contrib.auth.models import User
from badukroom.settings import MEDIA_ROOT
#from django.core.files.storage import FileSystemStorage

#my_store = FileSystemStorage(location='/static/sgf')

#user and pass is 'tfg' for admin

# Create your models here.

class Jugador(models.Model):
    nombre=models.CharField(max_length=50)
        
    def __unicode__(self):
        return self.nombre

class Partida(models.Model):
    fecha = models.DateField()
    jugador_negro = models.ForeignKey(Jugador, related_name='Jugador_jugador_negro')
    jugador_blanco = models.ForeignKey(Jugador, related_name='Jugador_jugador_blanco')
    resultado = models.CharField(max_length=50)
    #path = models.CharField(max_length=70)
    fichero = models.FileField(upload_to=MEDIA_ROOT)
    class Meta:
        unique_together=('jugador_negro', 'jugador_blanco','fecha')
    
    def __unicode__(self):
        return self.jugador_blanco.__unicode__()+" - "+self.jugador_negro.__unicode__()+" ["+unicode(self.fecha)+"]"
    