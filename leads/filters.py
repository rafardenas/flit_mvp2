from django.forms import widgets
from .models import Viajes
from django_filters import rest_framework as filters
from django.forms.widgets import NumberInput, Select
from crispy_forms.helper import FormHelper

class ViajesFilter(filters.FilterSet):
    

    CHOICES = (
        ("0","Esperando al transportista"),
        ("1","Inicio del flete"),
        ("2","En camino a recolección"),
        ("3","Recolección completada"),
        ("4","En ruta"),
        ("5","Descargando"),
        ("6","Flete Completado"),
    )

    def origen_choices(request):
        return 

    f_salida = filters.DateFilter(label="Fecha de Salida", widget=NumberInput(attrs={'type':'date', 'style': 'width:150px'}))
    status = filters.ChoiceFilter(label="Estatus", choices=CHOICES, method="status_filtering", widget=Select(attrs={'style': 'width:100px'}))
    origen = filters.ModelChoiceFilter(label="Origen", queryset=Viajes.objects.values_list('origen', flat=True).distinct(), widget=Select(attrs={'style': 'width:100px'}))
    destino = filters.ModelChoiceFilter(label="Destino", queryset=Viajes.objects.values_list('destino', flat=True).distinct(), widget=Select(attrs={'style': 'width:100px'}))
        
    class Meta:
        model = Viajes
        fields = ['f_salida', 'status', 'origen', 'destino']

    def status_filtering(self, queryset, name, value):
        return queryset.filter(status=value)

class horizontal_form(ViajesFilter):
    def __init__(self, *args, **kwargs):
        super(horizontal_form, self).__init__(*args, **kwargs)
        self.helper = FormHelper()  
        self.helper.form_class = 'form-horizontal'

