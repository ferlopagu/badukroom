from django.conf.urls import patterns, include, url
from django.contrib import admin
#ultimo add
from django.conf.urls.static import static
from django.conf import settings
from login import views

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'badukroom.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    #url(r'^$', principal.views.index, name='index'),
    #url(r'^$', include('login.urls', namespace="login")),
    url(r'^$', views.login_view, name='login_view'), #la viesta no se puede crear ni llamar login porque intercede con la que trae django
    url(r'^confirm/(?P<confirmation_code>\w+)/(?P<username>\w+)/', views.confirm, name="confirm"),
    #url(r'^$', views.login_view, name='login_view'), #la viesta no se puede crear ni llamar login porque intercede con la que trae django
    url(r'^baduk/', include('principal.urls', namespace="principal")),
    url(r'^logout/', views.logout_view, name='logout_view'),
    url(r'^redsocial/', include('redsocial.urls', namespace="redsocial")),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
    
)+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
