'''
Created on 26/12/2014

@author: fla2727
'''
from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from login.models import Perfil


class UserForm(UserCreationForm):
    error_css_class = 'error'
    required_css_class = 'required'
    email=forms.EmailField(required=True)
    #date = forms.DateField(label='Ej: 12/02/92', widget=forms.DateInput)
    
    class Meta:
        model=User
        fields=("first_name","last_name","username", "email", "password1", "password2")
    
    def save(self, commit=True):
        user=super(UserCreationForm,self).save(commit=False)
        email = self.cleaned_data['email']
        user.email=email
        
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email already exists")
        
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

class PerfilForm(ModelForm):
    
    #fecha_nacimiento=forms.DateField(label="Fecha nacimiento (Ej: 12/02/1992)",required=True) #vamos a excluir fecha de nacimiento por defecto y redifinirla para modificar el label
    class Meta:
        model=Perfil
        exclude=['user','amigos']
        #exclude =['user','fecha_nacimiento']
    """
    def save(self, commit=True):
        perfil=super(PerfilForm, self).save(commit=False)
        perfil.fecha_nacimiento=self.cleaned_data["fecha_nacimiento"]
        if commit:
            perfil.save()
        return perfil
    """
