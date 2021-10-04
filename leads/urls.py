from django.urls import path
from .views import (LeadListView, LeadDetailView, LeadUpdateView, 
    LeadDeleteView, AssignAgentView, CategoryListView, CategoryDetailView, LeadCategoryUpdateView, InicioViajeView, FinViajeView,
    EnConstruccionView, LeadCreateView, AyudaView, AyudaGralView, PreRegistroView
    )


app_name = "leads"

urlpatterns = [
    path('', LeadListView.as_view(), name='lead-list'),
    path('<int:pk>/', LeadDetailView.as_view(), name='lead-detail'),
    path('<int:pk>/delete/', LeadDeleteView.as_view(), name='lead-delete'),
    path('<int:pk>/update/', LeadUpdateView.as_view(), name='lead-update'),
    path('<int:pk>/assign-agent/', AssignAgentView.as_view(), name='assign-agent'),       
    path('<int:pk>/category/', LeadCategoryUpdateView.as_view(), name='lead-category-update'),       
    path('categories/', CategoryListView.as_view(), name='category-list'),       
    path('categories/<int:pk>/', CategoryDetailView.as_view(), name='category-detail'),       
    path('<int:pk>/inicio-viaje', InicioViajeView.as_view(), name='inicio-viaje'),       
    path('<int:pk>/fin-viaje', FinViajeView.as_view(), name='fin-viaje'),       
    path('create/', LeadCreateView.as_view(), name='lead-create'),       
    path('<int:pk>/ayuda', AyudaView.as_view(), name='ayuda'),       
    path('help', AyudaGralView.as_view(), name='ayuda-gral'),
    path('transportistas', EnConstruccionView.as_view(), name='transportistas'),
    path('embarcadores', EnConstruccionView.as_view(), name='embarcadores'),
    path('preregister', PreRegistroView.as_view(), name='preregistro'),

]