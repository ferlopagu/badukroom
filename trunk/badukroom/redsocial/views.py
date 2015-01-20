from django.shortcuts import render
from django.shortcuts import render_to_response
from django.core.context_processors import request

# Create your views here.
def inicio(request):
    return render_to_response('inicio.html', locals())