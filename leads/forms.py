from typing import Optional
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UsernameField, AuthenticationForm
from django.db.models import fields
from django.forms.widgets import NumberInput
from .models import Viajes, Agent, Ayuda, PreRegistro
from datetime import date
from django.forms.widgets import NumberInput


# Return the User model that is active in this project.
User = get_user_model()

class LeadModelForm(forms.ModelForm):
    f_salida = forms.DateField(label='Fecha de Salida', initial= date.strftime(date.today(), '%d/%m/%y'),  widget=NumberInput(attrs={'type':'date'})) 
    f_llegada = forms.DateField(label='Fecha de Llegada', initial= date.strftime(date.today(), '%d/%m/%y'), widget=NumberInput(attrs={'type':'date'}))

    class Meta:
        model = Viajes
        fields = [
            'origen',
            'destino',
            'f_salida',
            'f_llegada',    
            'tipo_embarque',
            'mercancia',
            'cantidad',
            'cantidad_tipo',
        ]



#class LeadForm(forms.Form):
#    first_name = forms.CharField()
#    last_name = forms.CharField()
#    age = forms.IntegerField(min_value=0)

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username",)
        field_classes = {'username': UsernameField}




class AssignAgentForm(forms.Form):
    agent = forms.ModelChoiceField(queryset=Agent.objects.none())

    def __init__(self, *args, **kwargs):
        request = kwargs.pop("request")
        agents = Agent.objects.filter(organisation=request.user.userprofile)
        super(AssignAgentForm, self).__init__(*args, **kwargs)
        self.fields['agent'].queryset = agents


class LeadCategoryUpdateForm(forms.ModelForm):
    class Meta:
        model = Viajes
        fields = (
            'category',
        )
        
class AyudaForm(forms.ModelForm):
    name = forms.CharField(label="Nombre", initial = "")
    flete_id = forms.CharField(label="Clave del Flete", initial = "")
    metodo_contacto = forms.CharField(label="Método preferido de contacto")
    asunto = forms.CharField(label="Asunto")
    mensaje = forms.CharField(label="Mensaje")
    
    class Meta:
        model = Ayuda
        fields = '__all__'
    
class CustomAuthenticationForm(AuthenticationForm):
    username = UsernameField(
        label='Nombre de Usuario',
        widget=forms.TextInput(attrs={'autofocus': True})
    )
    password = forms.CharField(
        label=("Contraseña"),
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'current-password'}),
    )

class PreRegistroForm(forms.ModelForm):
    ROLES = (
        ('Transportista', 'Transportista'),
        ('Embarcador', 'Embarcador'),
    )

    first_name = forms.CharField(label="Nombre", initial = "")
    last_name = forms.CharField(label="Apellido", initial = "")
    email = forms.EmailField(label="Correo Electrónico")
    telefono = forms.IntegerField(required=False)
    rol = forms.ChoiceField(label="Selecciona", choices=ROLES)
    compania = forms.CharField(label="Compañia")

    class Meta:
        model = PreRegistro
        fields = '__all__'