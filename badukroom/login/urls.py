'''
Created on 25/12/2014

@author: fla2727
'''
from django.conf.urls import patterns, url
from login import views

urlpatterns = patterns ('' ,
    url(r'^$', views.login_view, name='login_view'), #la viesta no se puede crear ni llamar login porque intercede con la que trae django
    #url(r'^login/', views.login, name='login2'),
)