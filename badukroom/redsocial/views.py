from django.shortcuts import render
from django.shortcuts import render_to_response
from django.core.context_processors import request
from django.contrib.auth.decorators import login_required
from django.template.context import RequestContext

# Create your views here.
@login_required(login_url='/login')
def inicio(request):
    #return render_to_response('inicio.html', locals())
    return render_to_response('inicio.html',context_instance=RequestContext(request))
    