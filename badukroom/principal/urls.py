'''
Created on 25/12/2014

@author: fla2727
'''
from django.conf.urls import patterns, url
from principal import views

urlpatterns = patterns ('' ,
    url(r'^$', views.login, name='login'),
    url(r'^index/', views.index, name='index'),
)