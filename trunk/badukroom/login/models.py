from django.db import models
from django.contrib.auth.models import User
from principal.models import Jugador 
from distutils.command.upload import upload
from badukroom.settings import MEDIA_ROOT
import random
import string

rango=[("30k","30k"), ("29k","29k"), ("28k","28k"),("27k","27k"),("26k","26k"),("25k","25k"),("24k","24k"),("23k","23k"),("22k","22k"),("21k","21k"),("20k","20k"),("19k","19k"),("18k","18k"),("17k","17k"),("16k","16k"),("15k","15k"),("14k","14k"),("13k","13k"),("12k","12k"),("11k","11k"),("10k","10k"),("9k","9k"),("8k","8k"),("7k","7k"),("6k","6k"),("5k","5k"),("4k","4k"),("3k","3k"),("2k","2k"),("1k","1k"),("1D","1D"),("2D","2D"),("3D","3D"),("4D","4D"),("5D","5D"),("6D","6D"),("7D","7D"),("8D","8D"),("9D","9D"),]

class Perfil(models.Model):
    user=models.OneToOneField(User, unique=True)
    fecha_nacimiento=models.DateField(help_text="Formato: dd/mm/yyyy")
    rango = models.CharField(max_length=50, choices=rango)
    jugadores_favoritos=models.ManyToManyField(Jugador,  blank=True)
    foto_principal=models.ImageField( blank=True, upload_to=MEDIA_ROOT+'imagenes', default=MEDIA_ROOT+"/imagenes/sin_foto.jpg")
    #path_principal=models.FilePathField(path=MEDIA_ROOT+'imagenes')
    #default=MEDIA_ROOT+'imagenes/'+foto_principal.name.__str__()
    path_principal = models.CharField(max_length=70, default='imagenes/sin_foto.jpg', blank=True)
    foto_portada=models.ImageField( blank=True, upload_to=MEDIA_ROOT+'imagenes', default=MEDIA_ROOT+"/imagenes/sin_portada.jpg")
    path_portada = models.CharField(max_length=70, default='imagenes/sin_portada.jpg' ,blank=True)
    #path_portada=models.FilePathField(path=MEDIA_ROOT+'imagenes')
    amigos=models.ManyToManyField('self',  blank=True)
    
    def __unicode__(self):
        return self.user.username
    
    def save(self, *args, **kwargs):
        #Observamos cambios en la foto principal por si tenemos que actualizar foto y path
        array=self.foto_principal.name.split("/")
        nombre_fichero=array[len(array)-1]
        if self.path_principal != 'imagenes/'+nombre_fichero:
            if self.path_principal == "" or self.path_principal==None or self.foto_principal==None:
                self.path_principal='imagenes/sin_foto.jpg'
            else:
                self.foto_principal.name=''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(3))+nombre_fichero #add principio random
                path_principal="imagenes/"+self.foto_principal.name
                #self.path_principal = 'imagenes/'+self.foto_principal.name.__str__() #Sobreescribimos el save para que actualice el path con el nombre del fichero
                self.path_principal=path_principal
        #Observamos cambios en la foto portada por si tenemos que actualizar foto y path    
        array=self.foto_portada.name.split("/")
        nombre_portada=array[len(array)-1]
        if self.path_portada != 'imagenes/'+nombre_portada: 
            if self.path_portada == "" or self.path_portada==None or self.foto_portada==None:
                self.path_portada='imagenes/sin_portada.jpg'
            else:
                self.foto_portada.name=''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(3))+nombre_portada #add principio random
                path_portada="imagenes/"+self.foto_portada.name
                #self.path_principal = 'imagenes/'+self.foto_principal.name.__str__() #Sobreescribimos el save para que actualice el path con el nombre del fichero
                self.path_portada=path_portada
        #super(Perfil, self).save()
        #Guardamos cambios
        super(Perfil, self).save(*args, **kwargs)
    
    def delete(self, *args, **kwargs):
        user=self.user
        self.foto_portada.delete()
        self.foto_principal.delete()
        super(Perfil, self).delete(*args, **kwargs)
        user.delete() #al borrar el perfil borramos tambien el usuario