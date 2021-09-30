from django.urls import path
from .views import (LeadListView, LeadDetailView, LeadUpdateView, 
    LeadDeleteView, AssignAgentView, CategoryListView, CategoryDetailView, LeadCategoryUpdateView, InicioViajeView, FinViajeView,
    EnConstruccionView, LeadCreateView, AyudaView, AyudaGralView
    )


app_name = "leads"

urlpatterns = [
    path('', LeadListView.as_view(), name='lead-list'),
    path('<int:pk>/', LeadDetailView.as_view(), name='lead-detail'),
    path('<slug:pk>/delete/', LeadDeleteView.as_view(), name='lead-delete'),
    path('<slug:pk>/update/', LeadUpdateView.as_view(), name='lead-update'),
    path('<slug:pk>/assign-agent/', AssignAgentView.as_view(), name='assign-agent'),       
    path('<slug:pk>/category/', LeadCategoryUpdateView.as_view(), name='lead-category-update'),       
    path('categories/', CategoryListView.as_view(), name='category-list'),       
    path('categories/<slug:pk>/', CategoryDetailView.as_view(), name='category-detail'),       
    path('<slug:pk>/inicio-viaje', InicioViajeView.as_view(), name='inicio-viaje'),       
    path('<slug:pk>/fin-viaje', FinViajeView.as_view(), name='fin-viaje'),       
    path('create/', LeadCreateView.as_view(), name='lead-create'),       
    path('<slug:pk>/ayuda', AyudaView.as_view(), name='ayuda'),       
    path('help', AyudaGralView.as_view(), name='ayuda-gral'),
    path('transportistas', EnConstruccionView.as_view(), name='transportistas'),
    path('embarcadores', EnConstruccionView.as_view(), name='embarcadores'),

]