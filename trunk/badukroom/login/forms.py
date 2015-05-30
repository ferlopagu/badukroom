'''
Created on 26/12/2014

@author: fla2727
'''
from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from login.models import Perfil
from django.forms.widgets import PasswordInput
import re
import datetime

class UserForm(UserCreationForm):
    error_css_class = 'error'
    required_css_class = 'required'
    email=forms.EmailField(required=True)
  
    class Meta:
        model=User
        fields=("first_name","last_name","username", "email", "password1", "password2")
    
    def save(self, commit=True):
        user=super(UserForm, self).save(commit=False)
        email = self.cleaned_data['email']
        user.email=email
        username=self.cleaned_data['username']
        
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Ya existe usuario con ese email")
        patron = re.compile('\w+@\w+\.\w+')
        if patron.match(email)==None:
            raise forms.ValidationError('El email no esta bien escrito, ej: prueba@prueba.com')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Ya existe un usuario con ese nick")
        if username == "":
            raise forms.ValidationError("El nick no puede ser vacio")
        
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user
    
    def clean_email(self):
        email=self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Ya existe usuario con este email')
        patron = re.compile('\w+@\w+\.\w+')
        if patron.match(email)==None:
            raise forms.ValidationError('El email no esta bien escrito, ej: prueba@prueba.com')
        return email
    
    def clean_username(self):
        print "ENTRAMOS EN CLEAN_USERNAME"
        username=self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Ya existe un usuario con ese nick")
        if username == "":
            raise forms.ValidationError("El nick no puede ser vacio")
        return username 


class PerfilForm(ModelForm):
    error_css_class = 'error'
    required_css_class = 'required'
    
    class Meta:
        model=Perfil
        fields=("fecha_nacimiento","ciudad","rango", "jugadores_favoritos", "foto_portada", "foto_principal")

class UserForm2(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name')