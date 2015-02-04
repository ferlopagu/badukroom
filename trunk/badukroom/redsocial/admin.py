from django.contrib import admin
from redsocial.models import Comentario, Respuesta, PeticionAmistad
# Register your models here.
admin.site.register(Comentario)
admin.site.register(Respuesta)
admin.site.register(PeticionAmistad)