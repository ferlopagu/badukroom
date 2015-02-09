'''
Created on 26/12/2014

@author: fla2727
'''
from django import forms
from django.forms import ModelForm
from redsocial.models import Comentario, Respuesta

"""
class ComentarioForm(ModelForm):
    class Meta:
        model=Comentario
        exclude =['perfil', 'fecha', 'partida']
"""

class RespuestaForm(ModelForm):
    class Meta:
        model=Respuesta
        exclude =['perfil','fecha']


class ComentarioForm(forms.Form):
    texto=forms.CharField(label="Tu comentario", max_length=2000)
    fichero=forms.FileField(label="Sgf", required=False)