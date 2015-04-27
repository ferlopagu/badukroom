'''
Created on 27/4/2015

@author: fla2727

class Comentario(models.Model):
    fecha=models.DateTimeField()
    perfil=models.ForeignKey(Perfil)
    texto=models.TextField()


'''
import random
import string
import datetime
from login.models import Perfil
from redsocial.models import Comentario, Respuesta
def cargaComentariosRelleno():
    i=0
    print "=====EMPEZANDO CARGA======"
    while i < 20:
        texto="Comentario "+str(i)+'  '.join(random.choice(string.ascii_lowercase) for x in range(350))
        fecha=datetime.datetime.now()
        #total = Perfil.objects.all().count()
        #id=random.randrange(0,total-1)
        perfil = Perfil.objects.get(user__username='priscilacb')
        comentario = Comentario(fecha=fecha, perfil=perfil, texto=texto)
        comentario.save()
        print comentario.__unicode__()
        j=0
        while j<3:
            perfil2 = Perfil.objects.get(user__username='fla2727')
            texto2="Respuesta a comentario "+str(i)+' - '+str(j)+'   '.join(random.choice(string.ascii_lowercase) for x in range(350))
            respuesta=Respuesta(fecha=fecha, perfil=perfil2, texto=texto2, comentario=comentario)
            respuesta.save()
            j+=1
            print "Respuesta: "+str(j)
        i+=1
    print "=======CARGA FINALIZADA====="

if __name__ == '__main__':
    import django
    django.setup()
    cargaComentariosRelleno()