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

def login_view(request):
    login_incorrecto=""
    if request.method=='POST':
        formulario_login=AuthenticationForm(request.POST)
        user_form=UserForm(request.POST)
        perfil_form=PerfilForm(request.POST, request.FILES)
        if 'entrar' in request.POST:
            print "Entro en entrar"
            if formulario_login.is_valid:
                usuario=request.POST['username']
                clave=request.POST['password']
                acceso=authenticate(username=usuario, password=clave)
                if acceso is not None:
                    if acceso.is_active:
                        login(request, acceso)
                        return HttpResponseRedirect('/redsocial')
                    else:
                        return render_to_response('noactivo.html', context_instance=RequestContext(request))
                else:
                    print "el formulario es valido pero acceso es not"
                    login_incorrecto="El nick o password no son validos."
                    formulario_login=AuthenticationForm()
                    user_form = UserForm()
                    perfil_form=PerfilForm()
                    return render_to_response('login.html', {'formulario_login':formulario_login, 'user_form':user_form, 'perfil_form':perfil_form, 'login_incorrecto':login_incorrecto} ,context_instance=RequestContext(request) )
                    #return render_to_response('nousuario.html', context_instance=RequestContext(request))
        elif 'registrar' in request.POST:
            print "Entro en registrar"
            if user_form.is_valid() and perfil_form.is_valid():
                print "userform y perfilform son validos"
                print request.FILES
                user=user_form.save() #guardamos el usuario
                perfil=perfil_form.save(commit=False) #tenemos que add el usuario
                perfil.user=user #add el usuario al perfil 
                perfil.save() #guardamos el perfil
                return HttpResponseRedirect('/')
        else:
            return HttpResponseRedirect('/quedise')
            
    else:
        formulario_login=AuthenticationForm()
        user_form = UserForm()
        perfil_form=PerfilForm()
    return render_to_response('login.html', {'formulario_login':formulario_login, 'user_form':user_form, 'perfil_form':perfil_form, 'login_incorrecto':login_incorrecto}, context_instance=RequestContext(request))
