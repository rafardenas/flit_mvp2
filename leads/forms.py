from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UsernameField
from .models import Viajes, Agent
from datetime import date


# Return the User model that is active in this project.
User = get_user_model()

class LeadModelForm(forms.ModelForm):
    f_salida = forms.DateField(label='Fecha de Salida', initial= date.strftime(date.today(), '%d/%m/%y'), input_formats=['%d/%m/%y']) 
    f_llegada = forms.DateField(label='Fecha de Llegada', initial= date.strftime(date.today(), '%d/%m/%y'), input_formats=['%d/%m/%y'])
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
        