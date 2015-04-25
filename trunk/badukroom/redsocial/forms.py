'''
Created on 26/12/2014

@author: fla2727
'''
from django import forms
from django.forms import ModelForm
from redsocial.models import Comentario, Respuesta, Grupo, PeticionRevision
from principal.models import Revisor
import datetime
from datetime import date
from django.db.models import Q
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
    texto=forms.CharField(label="Tu comentario", max_length=5000, required=False, widget=forms.Textarea)
    fichero=forms.FileField(label="Sgf", required=False)

class GrupoForm(ModelForm):
    class Meta:
        model=Grupo
        exclude=['miembros', 'path_portada']

class EnvioForm(forms.Form):
    fichero=forms.FileField(label="Sgf", required=True)
    revisor=forms.ModelChoiceField(Revisor.objects.exclude(Q(perfil=PeticionRevision.objects.values("receptor")))) #Excluimos a los revisores opcupados

class SgfForm(forms.Form):
    fichero=forms.FileField(label="Sgf", required=True)

class FechasForm(forms.Form):
    inicio=forms.DateField(initial='01/01/1875',required=True)
    fin=forms.DateField(initial=datetime.datetime.now(),required=True)

class MensajeForm(forms.Form):
    texto=forms.CharField(label="Mensaje", max_length=2000, required=True)