'''
Created on 26/12/2014

@author: fla2727
'''
from django import forms
from django.forms import ModelForm
from redsocial.models import Comentario, Respuesta

class ComentarioForm(ModelForm):
    class Meta:
        model=Comentario
        exclude =['perfil', 'fecha']

class RespuestaForm(ModelForm):
    class Meta:
        model=Respuesta
        exclude =['perfil','fecha']
