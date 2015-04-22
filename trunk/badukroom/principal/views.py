from django.shortcuts import render
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.template import RequestContext
#from principal.forms import PartidaForm
from login.models import Perfil
# Create your views here.

def index(request):
    return render_to_response('index.html', locals())

def crea_partida(request):
    if request.method=='POST':
        #partida_form=PartidaForm(request.POST)
        partida_form=None
        if partida_form.is_valid() :
            partida_form.save() #guardamos el perfil
            return HttpResponseRedirect('/')
    else:
        #partida_form=PartidaForm()
        partida_form=None
    return render_to_response('crea_partida.html', {'partida_form':partida_form}, context_instance=RequestContext(request))

