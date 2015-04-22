from django.contrib import admin
from principal.models import Jugador, Partida, Revisor, Sgf, PartidaRevisada
# Register your models here.

admin.site.register(Jugador)
admin.site.register(Partida)
admin.site.register(Sgf)
admin.site.register(PartidaRevisada)
admin.site.register(Revisor)
