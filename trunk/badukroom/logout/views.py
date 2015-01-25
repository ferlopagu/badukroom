from django.shortcuts import render
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
# Create your views here.

@login_required(login_url='/login')
def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/')