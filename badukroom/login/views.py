from django.shortcuts import render

# Create your views here.
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from login.forms import UserForm, PerfilForm
from django.http import HttpResponseRedirect

#ultimos add
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required


def holaMundo(request):
    return render_to_response('mundo.html', locals())

def login2(request):
    if request.method=='POST':
        formulario_login=AuthenticationForm(request.POST)
        user_form=UserForm(request.POST)
        perfil_form=PerfilForm(request.POST)
        if formulario_login.is_valid:
            pass
            """
            usuario=request.POST['username']
            clave=request.POST['password']
            acceso=authenticate(username=usuario, password=clave)
            if acceso is not None:
                if acceso.is_active:
                    login(request, acceso)
                    return HttpResponseRedirect('/privado')
                else:
                    return render_to_response('noactivo.html', context_instance=RequestContext(request))
            else:
                return render_to_response('nousuario.html', context_instance=RequestContext(request))
                """
        elif user_form.is_valid() and perfil_form.is_valid():
            user=user_form.save() #guardamos el usuario
            perfil=perfil_form.save(commit=False) #tenemos que add el usuario
            perfil.user=user #add el usuario al perfil
            perfil.save() #guardamos el perfil
            return HttpResponseRedirect('/login')
        else:
            return HttpResponseRedirect('/blabla')
            
    else:
        formulario_login=AuthenticationForm()
        user_form = UserForm()
        perfil_form=PerfilForm()
    return render_to_response('login.html', {'formulario_login':formulario_login, 'user_form':user_form, 'perfil_form':perfil_form}, context_instance=RequestContext(request))

def registro(request):
    if request.method=='POST':
        user_form=UserForm(request.POST)
        perfil_form=PerfilForm(request.POST)
        #formulario=UserCreationForm(request.POST)
        #pdb.set_trace()
        if user_form.is_valid() and perfil_form.is_valid():
            user=user_form.save() #guardamos el usuario
            perfil=perfil_form.save(commit=False) #tenemos que add el usuario
            perfil.user=user #add el usuario al perfil
            perfil.save() #guardamos el perfil
            return HttpResponseRedirect('/')
    else:
        user_form = UserForm()
        perfil_form=PerfilForm()
    return render_to_response('formulario_usuario.html', {'user_form':user_form, 'perfil_form':perfil_form}, context_instance=RequestContext(request))

def login(request):
    #if not request.user.is_anonymous():
        #return HttpResponseRedirect('/privado')
    if request.method=='POST':
        formulario_login=AuthenticationForm(request.POST)
        if formulario_login.is_valid:
            usuario=request.POST['username']
            clave=request.POST['password']
            acceso=authenticate(username=usuario, password=clave)
            if acceso is not None:
                if acceso.is_active:
                    login(request, acceso)
                    return HttpResponseRedirect('/privado')
                else:
                    return render_to_response('noactivo.html', context_instance=RequestContext(request))
            else:
                return render_to_response('nousuario.html', context_instance=RequestContext(request))
    else:
        formulario_login=AuthenticationForm()
    return render_to_response('login.html', {'formulario_login':formulario_login}, context_instance=RequestContext(request))

@login_required(login_url='/ingresar')
def logout(request):
    logout(request)
    return HttpResponseRedirect('/')