'''
Created on 26/12/2014

@author: fla2727
'''
from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from principal.models import Perfil

class UserForm(UserCreationForm):
    email=forms.EmailField(required=True)
    
    class Meta:
        model=User
        fields=("first_name","last_name","username", "email", "password1", "password2")
    
    def save(self, commit=True):
        user=super(UserCreationForm,self).save(commit=False)
        user.email=self.cleaned_data["email"] #añadir el campo email al usuario
        user.set_password(self.cleaned_data["password1"]) #sino la password no se guarda cifrada
        if commit:
            user.save()
        return user

class PerfilForm(ModelForm):
    class Meta:
        model=Perfil
        exclude =['user']
