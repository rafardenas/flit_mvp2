from django.contrib import admin

# Register your models here.

from .models import User, Agent, UserProfile, Category, Viajes    

admin.site.register(User)
admin.site.register(Category)
admin.site.register(UserProfile)
admin.site.register(Viajes)
admin.site.register(Agent)
