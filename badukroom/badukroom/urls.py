from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'badukroom.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    #url(r'^$', principal.views.index, name='index'),
    url(r'^baduk/', include('principal.urls', namespace="principal")),
    url(r'^login/', include('principal.urls', namespace="login")),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
