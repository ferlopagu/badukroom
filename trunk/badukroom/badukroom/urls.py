from django.conf.urls import patterns, include, url
from django.contrib import admin
#ultimo add
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'badukroom.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    #url(r'^$', principal.views.index, name='index'),
    url(r'^baduk/', include('principal.urls', namespace="principal")),
    url(r'^login/', include('login.urls', namespace="login")),
    url(r'^$', include('redsocial.urls', namespace="redsocial")),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
)+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
