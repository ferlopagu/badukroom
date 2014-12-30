from django.db import models
from django.contrib.auth.models import User

#user and pass is 'tfg' for admin

rango=[("30k","30k"), 
       ("29k","29k"), 
       ("28k","28k"),
       ("27k","27k"),
       ("26k","26k"),
       ("25k","25k"),
       ("24k","24k"),
       ("23k","23k"),
       ("22k","22k"),
       ("21k","21k"),
       ("20k","20k"),
       ("19k","19k"),
       ("18k","18k"),
       ("17k","17k"),
       ("16k","16k"),
       ("15k","15k"),
       ("14k","14k"),
       ("13k","13k"),
       ("12k","12k"),
       ("11k","11k"),
       ("10k","10k"),
       ("9k","9k"),
       ("8k","8k"),  
       ("7k","7k"),
       ("6k","6k"),
       ("5k","5k"),
       ("4k","4k"),
       ("3k","3k"),
       ("2k","2k"),
       ("1k","1k"),
       ("1D","1D"),
       ("2D","2D"),
       ("3D","3D"),
       ("4D","4D"),
       ("5D","5D"),
       ("6D","6D"),
       ("7D","7D"),
       ("8D","8D"),
       ("9D","9D"),
       ]

# Create your models here.

class Jugador(models.Model):
    nombre=models.CharField(max_length=50)
        
    def __unicode__(self):
        return self.nombre

class Perfil(models.Model):
    user=models.OneToOneField(User, unique=True)
    fecha_nacimiento=models.DateField()
    rango = models.CharField(max_length=50, choices=rango)
    jugadores_favoritos=models.ManyToManyField(Jugador)
    def __unicode__(self):
        return self.user.username

class Partida(models.Model):
    fecha = models.DateField()
    jugador_negro = models.ForeignKey(Jugador, related_name='Jugador_jugador_negro')
    jugador_blanco = models.ForeignKey(Jugador, related_name='Jugador_jugador_blanco')
    resultado = models.CharField(max_length=50)
    path = models.CharField(max_length=70)
    
    class Meta:
        unique_together=('jugador_negro', 'jugador_blanco','fecha')
    
    def __unicode__(self):
        return self.jugador_blanco.__unicode__()+" - "+self.jugador_negro.__unicode__()+" ["+unicode(self.fecha)+"]"
    