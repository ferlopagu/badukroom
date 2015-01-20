'''
Created on 21/01/2015

@author: fla2727
'''
from django.conf.urls import patterns, url
from redsocial import views

urlpatterns = patterns ('' ,
    url(r'^$', views.inicio, name='inicio'),
    #url(r'^login/', views.login, name='login2'),
)