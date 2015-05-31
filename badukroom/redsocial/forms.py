'''
Created on 26/12/2014

@author: fla2727
'''
from django import forms
from django.forms import ModelForm
from redsocial.models import Grupo, PeticionRevision
from principal.models import Revisor
import datetime
from django.db.models import Q
from django.core.exceptions import ValidationError


class ComentarioForm(forms.Form):
    texto=forms.CharField(label="Tu comentario", max_length=5000, required=True, widget=forms.Textarea)
    fichero=forms.FileField(label="Sgf", required=False)

class GrupoForm(ModelForm):
    class Meta:
        model=Grupo
        exclude=['miembros', 'path_portada']

class EnvioForm(forms.Form):
    fichero=forms.FileField(label="Sgf")
    revisor=forms.ModelChoiceField(Revisor.objects.exclude(Q(perfil=PeticionRevision.objects.values("receptor")))) #Excluimos a los revisores opcupados
    
    def clean_fichero(self):
        print "Entramos en metodo"
        data = self.cleaned_data['fichero']
        print data
        if data == None:
            raise forms.ValidationError("No hay fichero!")
        return data
    
class SgfForm(forms.Form):
    fichero=forms.FileField(label="Sgf")

class FechasForm(forms.Form):
    inicio=forms.DateField(initial='01/01/1875',required=True)
    fin=forms.DateField(initial=datetime.datetime.now(),required=True)

class MensajeForm(forms.Form):
    texto=forms.CharField(label="Mensaje", max_length=2000, required=True)
