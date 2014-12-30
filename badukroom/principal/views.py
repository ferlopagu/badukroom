from django.shortcuts import render
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.template import RequestContext
# Create your views here.

def index(request):
    return render_to_response('index.html', locals())

def login(request):
    return render_to_response('login.html', locals())

def ingresar(request):
    if not request.user.is_anonymous():
        return HttpResponseRedirect('/index')
    if request.method=='POST':
        formulario=AuthenticationForm(request.POST)
        if formulario.is_valid:
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
        formulario=AuthenticationForm()
    return render_to_response('login.html', {'formulario': formulario},context_instance=RequestContext(request))
    

def registrar(request):
    pass

def crea_usuario(request):
    if request.method=='POST':
        user_form=UserForm(request.POST)
        perfil_form=UsuarioForm(request.POST)
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
        perfil_form=UsuarioForm()
    return render_to_response('formulario_usuario.html', {'user_form':user_form, 'perfil_form':perfil_form}, context_instance=RequestContext(request))
