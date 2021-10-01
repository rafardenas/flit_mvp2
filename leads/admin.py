from django.contrib import admin

# Register your models here.

from .models import User, Agent, UserProfile, Category, Viajes, Imagenes_viajes, Ayuda, Operador, LineaTransporte, PreRegistro

admin.site.register(User)
admin.site.register(Category)
admin.site.register(UserProfile)
admin.site.register(Viajes)
admin.site.register(Agent)
admin.site.register(Imagenes_viajes)
admin.site.register(Ayuda)
admin.site.register(Operador)
admin.site.register(LineaTransporte)
admin.site.register(PreRegistro)

