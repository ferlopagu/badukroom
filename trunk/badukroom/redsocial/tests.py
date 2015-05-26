from django.test import TestCase

from django.contrib.auth.models import User
from login.models import Perfil
from redsocial.models import Comentario
import datetime
# Create your tests here.
class ComentarioTestCase(TestCase): 
    def setUp(self):
        fecha2=datetime.datetime.now()
        texto="Comentario"
        user1 = User.objects.create(username="priscilacb", password="", first_name="Priscila")
        perfil = Perfil.objects.create(user=user1, fecha_nacimiento=fecha2)
        Comentario.objects.create(fecha=fecha2, perfil=perfil, texto=texto)

    def test_comentario_texto(self):
        comentario = Comentario.objects.get(perfil__user__username="priscilacb")
        self.assertEqual(comentario.texto, "Comentario")