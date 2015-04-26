'''
Created on 25/12/2014

@author: fla2727
'''
from django.conf.urls import patterns, url
from login import views

#NO ESTAMOS USANDO ESTE FICHERO
urlpatterns = patterns ('' ,
    url(r'^confirm/(?P<confirmation_code>\w+)/(?P<username>\w+)/', views.confirm, name="confirm"),
    url(r'^$', views.login_view, name='login_view'), #la viesta no se puede crear ni llamar login porque intercede con la que trae django
    #url(r'^confirm/(?P<confirmation_code>\w+)/(?P<username>\w+)/', views.confirm, name="confirm"),
    #url(r'^login/', views.login, name='login2'),
)