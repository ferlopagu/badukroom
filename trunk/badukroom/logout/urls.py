'''
Created on 25/12/2014

@author: fla2727
'''
from django.conf.urls import patterns, url
from logout import views

urlpatterns = patterns ('' ,
    url(r'^$', views.logout_view, name='logout_view'),
)