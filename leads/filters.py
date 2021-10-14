from .models import Viajes
from django_filters import rest_framework as filters
from django.forms.widgets import NumberInput

class ViajesFilter(filters.FilterSet):
    class Meta:
        model = Viajes
        fields = ('f_llegada', 'status')

    CHOICES = (
        ("0","Esperando al transportista"),
        ("1","Inicio del flete"),
        ("2","En camino a recolección"),
        ("3","Recolección completada"),
        ("4","En ruta"),
        ("5","Descargando"),
        ("6","Flete Completado"),
    )

    f_llegada = filters.DateFilter(label="Fecha Llegada", widget=NumberInput(attrs={'type':'date'}))
    status = filters.ChoiceFilter(label="Estatus", choices=CHOICES, method="status_filtering")
        

    def status_filtering(self, queryset, name, value):
        expression = value
        return queryset.filter(status=expression)




