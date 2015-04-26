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

class UserForm(UserCreationForm):
    error_css_class = 'error'
    required_css_class = 'required'
    email=forms.EmailField(required=True)
    #date = forms.DateField(label='Ej: 12/02/92', widget=forms.DateInput)
    
    class Meta:
        model=User
        fields=("first_name","last_name","username", "email", "password1", "password2")
    
    
    def clean(self):
        cleaned_data = super(UserForm, self).clean()
        email=self.cleaned_data['email']
        print "IMPRIMO EMAIL EN METODO CLEAN"
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Ya existe usuario con ese email")
        #if self.cleaned_data['password'] != self.cleaned_data['confirm_password']:
            #self.add_error('confirm_password', 'Password & Confirm Password must match.')
        #return cleaned_data
    
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
    """
    def clean_email(self):
        email=self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Ya existe usuario con este email')
        patron = re.compile('\w+@\w+\.\w+')
        if patron.match(email)==None:
            raise forms.ValidationError('El email no esta bien escrito, ej: prueba@prueba.com')
        return self.cleaned_data['email']
    """
    """
    def clean_username(self):
        username=self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Ya existe un usuario con ese nick")
        if username == "":
            raise forms.ValidationError("El nick no puede ser vacio")
    """
    


class PerfilForm(ModelForm):
    error_css_class = 'error'
    required_css_class = 'required'
    
    #fecha_nacimiento=forms.DateField(label="Fecha nacimiento (Ej: 12/02/1992)",required=True) #vamos a excluir fecha de nacimiento por defecto y redifinirla para modificar el label
    class Meta:
        model=Perfil
        exclude=['user','amigos','path_portada','path_principal', 'confirmation_code']
        #exclude =['user','fecha_nacimiento']
    """
    def save(self, commit=True):
        perfil=super(PerfilForm, self).save(commit=False)
        perfil.fecha_nacimiento=self.cleaned_data["fecha_nacimiento"]
        if commit:
            perfil.save()
        return perfil
    """

class UserForm2(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name')
