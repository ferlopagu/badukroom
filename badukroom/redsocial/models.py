from django.db import models
from login.models import Perfil
from badukroom.settings import MEDIA_ROOT 
# Create your models here.

class Comentario(models.Model):
    fecha=models.DateTimeField()
    perfil=models.ForeignKey(Perfil)
    texto=models.CharField(max_length=2000)
    fichero=models.FileField(upload_to=MEDIA_ROOT+'sgf')
    
    def __unicode__(self):
        return self.perfil.user.username+" "+self.texto