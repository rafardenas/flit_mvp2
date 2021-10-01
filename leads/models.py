from django.db import models
from django.db.models.deletion import SET_NULL
from django.db.models.signals import post_save  # listens just before we commit to the database
from django.contrib.auth.models import AbstractUser
from datetime import date, datetime
import os
import random

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

    def pk_generator():
        chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        intss = '1234567890'
        # uncomment to use a more compley flete id
        #randomstr = ''.join((random.choice(chars)) for x in range(3)) + ''.join((random.choice(intss)) for x in range(4)) 
        randomint = ''.join((random.choice(intss)) for x in range(5)) 
        return 1

    id = models.CharField(default=pk_generator, primary_key=True, max_length=10, unique=True)
    origen = models.CharField(max_length=20)
    destino = models.CharField(max_length=20)
    f_salida = models.DateField(default=date.today)
    f_llegada = models.DateField(default=date.today)
    tipo_embarque = models.CharField(default=None, choices=TIPO_EMBARQUE, max_length=30)
    costo = models.CharField(default='0', max_length=20, blank=True, null=True)
    mercancia = models.CharField(max_length=20)
    cantidad = models.IntegerField(default=0)
    cantidad_tipo = models.CharField(default='Otro', choices=TIPO_CANTIDAD, max_length=30)
    status = models.CharField(default='0', choices=STATUS, max_length=30)
    operador = models.ForeignKey("Operador", null=True, blank=True, on_delete=models.SET_NULL)
    linea_transporte = models.ForeignKey("LineaTransporte", null=True, blank=True, on_delete=models.SET_NULL)

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
    added_time = models.DateTimeField(default=datetime.now)

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
    asunto = models.CharField(max_length=30, null=True, blank=True)
    mensaje = models.CharField(max_length=150)

class PreRegistro(models.Model):
    #ROLES = (
    #    ('Transportista', 'Quiero enviar mi mercancia con Flit'),
    #    ('Embarcador', 'Quiero trabajar como transportista en Flit'),
    #)

    ROLES = (
        ('Transportista', 'Transportista'),
        ('Embarcador', 'Embarcador'),
    )


    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    telefono = models.IntegerField(null=True, blank=True)
    rol = models.CharField(default=None, choices=ROLES, max_length=50)
    compania = models.CharField(max_length=50)
    
class Operador(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    phone = models.CharField(max_length=30)
    linea_transporte = models.ForeignKey("LineaTransporte", null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.linea_transporte}"  

class LineaTransporte(models.Model):
    name = models.CharField(max_length=30)
    rfc = models.CharField(max_length=30)
    contacto = models.CharField(max_length=30)    
    calle = models.CharField(max_length=20)    
    numero = models.CharField(max_length=20)    
    municipio = models.CharField(max_length=20)    
    ciudad = models.CharField(max_length=20)    
    cp = models.CharField(max_length=20)    
    estado = models.CharField(max_length=20)    


    def __str__(self):
        return f"{self.name}"

def post_user_created_signal(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

post_save.connect(post_user_created_signal, sender=User)
      

    