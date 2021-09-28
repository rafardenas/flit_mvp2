from django.db import models
from django.db.models.signals import post_save  # listens just before we commit to the database
from django.contrib.auth.models import AbstractUser
from datetime import date
import os

class User(AbstractUser):
    is_organisor = models.BooleanField(default=True) 
    is_agent = models.BooleanField(default=False) 

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username 

class Viajes(models.Model):
    TIPO_EMBARQUE = (
        ('Caja Seca', 'Caja Seca'),
        ('Tolva', 'Tolva'),
        ('Refrigerado', 'Refrigerado'),
    )

    TIPO_CANTIDAD = (
        ('Toneladas', 'Toneladas'),
        ('Tarimas', 'Tarimas'),
        ('Otro', 'Otro'),
    )

    STATUS = (
        ('0', '0'),
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
        ('5', '5'),
        ('6', '6'),
    )


    origen = models.CharField(max_length=20)
    destino = models.CharField(max_length=20)
    f_salida = models.DateField(default=date.today)
    f_llegada = models.DateField(default=date.today)
    tipo_embarque = models.CharField(default=None, choices=TIPO_EMBARQUE, max_length=30)
    mercancia = models.CharField(max_length=20)
    cantidad = models.IntegerField(default=0)
    cantidad_tipo = models.CharField(default='Otro', choices=TIPO_CANTIDAD, max_length=30)
    status = models.CharField(default='0', choices=STATUS, max_length=30)


    organisation = models.ForeignKey(UserProfile, on_delete=models.CASCADE)                # because the agent can be optional, we have to add this field as a way to filter the leads via the User profile
    agent = models.ForeignKey("Agent", null=True, blank=True, on_delete=models.SET_NULL)
    category = models.ForeignKey("Category", related_name="leads", blank=True, null=True, on_delete=models.SET_NULL)


    #SOURCE_CHOICES = (
    #    ('YouTube', 'YouTube'),
    #    ('Google', 'Google'),
    #    ('Newsletter', 'Newsletter')
    #)
    # This type of fields can help to show the progress of the shipment, other way to do it is on the front end directly
    # but the app would have to be deployed again. 
    #phoned = models.BooleanField(default=False)
    #source = models.CharField(choices=SOURCE_CHOICES, max_length=100)

    #profile_picture = models.ImageField(blank=True, null=True)
    #special_files = models.FileField(blank=True, null=True)

    def __str__(self):
        return f"{self.origen}  - {self.destino}"

class Imagenes_viajes(models.Model):
    CATEGORIA = (
        ('Recoleccion', 'Recoleccion'),
        ('Entrega', 'Entrega'),
        ('Otro', 'Otro'),
    )

    
    def photopath(self, filename):
        basefilename, file_extension= os.path.splitext(filename)
        return 'imagenes-fletes/{basename}-id-{fleteid}{ext}'.format(fleteid= self.flete.pk, basename=self.categoria, ext=file_extension)


    categoria  = models.CharField(default=None, choices=CATEGORIA, max_length=30)
    flete = models.ForeignKey(Viajes, on_delete=models.CASCADE)
    imagen = models.ImageField(default='default.jpg', upload_to=photopath)

    def __str__(self):
        return f"{self.flete}  - {self.categoria}"

    #def save(self, *args, **kwargs):
    #    super(Imagenes_viajes, self).save(*args, **kwargs)
    #    print(self.imagen.name)




class Agent(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # 'organisation' refers to the user that is logged in/the organisor
    organisation = models.ForeignKey(UserProfile, on_delete=models.CASCADE)      # if the user is deleted, the agent will be as well. 
    def __str__(self):
        return self.user.email


class Category(models.Model):
    name = models.CharField(max_length=30)     # New, Contacted, Unconverted, Converted.
    organisation = models.ForeignKey(UserProfile, on_delete=models.CASCADE) 

    def __str__(self):
        return self.name



class Ayuda(models.Model):
    name = models.CharField(max_length=50)
    flete_id = models.CharField(max_length=10)
    metodo_contacto = models.CharField(max_length=30)
    asunto = models.CharField(max_length=30)
    mensaje = models.CharField(max_length=150)

"""class PreRegistro(models.Model):
    name = 
    email = 
    rol = """




def post_user_created_signal(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

post_save.connect(post_user_created_signal, sender=User)
      

    