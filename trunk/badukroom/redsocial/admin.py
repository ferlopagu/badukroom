from django.contrib import admin
from redsocial.models import Comentario, Respuesta, PeticionAmistad, Notificacion, Grupo, PeticionRevision
from principal.models import PartidaRepositorio
# Register your models here.
admin.site.register(Comentario)
admin.site.register(Respuesta)
admin.site.register(PeticionAmistad)
admin.site.register(Notificacion)
admin.site.register(Grupo)
admin.site.register(PeticionRevision)
admin.site.register(PartidaRepositorio)