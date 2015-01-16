'''
Created on 26/12/2014

@author: fla2727
'''
from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from principal.models import Partida

class PartidaForm(ModelForm):
    class Meta:
        model=Partida
