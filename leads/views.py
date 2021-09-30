from django.core.mail import message, send_mail
from django.db.models import query
from django.db.models.query_utils import Q 
from django.http.response import HttpResponseRedirect
from django.shortcuts import render, redirect, reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.views import generic
from .models import Viajes, Agent, Category, Imagenes_viajes
from .forms import LeadModelForm, CustomUserCreationForm, AssignAgentForm, LeadCategoryUpdateForm, CustomAuthenticationForm, AyudaForm
from agents.mixins import OrganisorandLoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.db import IntegrityError
import random

# Create your views here.

class SignupView(generic.CreateView):
    template_name = 'registration/signup.html'
    form_class = CustomUserCreationForm
    
    def get_success_url(self):
        return reverse("login")


class LandingPageView(generic.TemplateView):
    template_name = 'landing.html'


class LeadListView(LoginRequiredMixin, generic.ListView):
    template_name = "leads/lead_list.html"
    context_object_name = "viajes"

    def get_queryset(self):
        # get the current user
        user = self.request.user   
        # initial queryset for the entire organisation (i.e. the agent or the organisor)
        if user.is_organisor:
            #query all the leads for certain organisation from the *organisation*
            queryset = Viajes.objects.filter(organisation=user.userprofile, 
                    agent__isnull=False)      #if the user is organisor, it will have a userprofile, otherwise that user is an agent.
            queryset = Viajes.objects.filter(organisation=user.userprofile)

        else:
            #query all the leads for certain organisation from the *agent* (note how the agent and the organisation are linked: a user can be an agent, and an agent has an organisation)
            queryset= Viajes.objects.filter(organisation=user.agent.organisation)
            #filter for the agent that is logged in. (agent__user is equivalent to: `agent.user` in flask)
            queryset = queryset.filter(agent__user = user   )

        return queryset

    def status_readable(status):
        dictStatus = {
            1: "Inicio del flete",
            2: "En camino a recolección",
            3: "Recolección completada",
            4: "En ruta",
            5: "Descargando",
            6: "Completado",
        }
        status_read = dictStatus[int(status)]
        return status_read



    def get_context_data(self, **kwargs):
        context = super(LeadListView, self).get_context_data(**kwargs)
        user = self.request.user 
        if user.is_organisor:
            queryset = Viajes.objects.filter(organisation=user.userprofile, agent__isnull=True)
            context.update({
                "otros_viajes": queryset
            })
        return context


class LeadDetailView(LoginRequiredMixin, generic.DetailView):
    template_name = "leads/lead_detail.html"
    queryset = Viajes.objects.all()
    context_object_name = 'viaje'

    def get_queryset(self):
        user = self.request.user      
        if user.is_organisor:
            queryset = Viajes.objects.filter(organisation=user.userprofile)      
        else:
            queryset= Viajes.objects.filter(organisation=user.agent.organisation)
            queryset = queryset.filter(agent__user == self.request.user)
        return queryset


class LeadCreateView(OrganisorandLoginRequiredMixin, generic.CreateView):
    template_name = "leads/lead_create.html"
    form_class = LeadModelForm    
    
    def get_success_url(self):
        return reverse("leads:lead-list")
    
    def pk_generator(self):
        chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        intss = '1234567890'
        # uncomment to use a str
        #randomstr = ''.join((random.choice(chars)) for x in range(3)) + ''.join((random.choice(intss)) for x in range(4)) 
        randomint = ''.join((random.choice(intss)) for x in range(5)) 
        return randomint

    def form_valid(self, form):
        lead = form.save(commit=False)
        print(lead)
        lead.organisation = self.request.user.userprofile
        try:
            lead.save()
        except IntegrityError:
            lead.pk = self.pk_generator()
            lead.save()     
        return super(LeadCreateView, self).form_valid(form)


class LeadUpdateView(OrganisorandLoginRequiredMixin, generic.UpdateView):
    template_name = "leads/lead_update.html"
    form_class = LeadModelForm
    context_object_name = 'viajes'

    def get_queryset(self):
        user = self.request.user      
        return Viajes.objects.filter(organisation=user.userprofile)      

    def get_success_url(self):
        return reverse("leads:lead-list")


class LeadDeleteView(OrganisorandLoginRequiredMixin, generic.DeleteView):
    template_name = "leads/lead_delete.html"
    
    def get_queryset(self):
        user = self.request.user      
        return Viajes.objects.filter(organisation=user.userprofile)    

    def get_success_url(self):
        return reverse("leads:lead-list")


class AssignAgentView(OrganisorandLoginRequiredMixin, generic.FormView):
    template_name = "leads/assign_agent.html"
    form_class = AssignAgentForm

    def get_form_kwargs(self, **kwargs):
        kwargs = super(AssignAgentView, self).get_form_kwargs(**kwargs)

        kwargs.update( {
            "request" : self.request
        })
        return kwargs
    
    def get_success_url(self):
        return reverse("leads:lead-list")

    def form_valid(self, form):
        # this method handles what happens when the form is submitted
        #print(self.kwargs)
        agent = form.cleaned_data["agent"]
        lead = Viajes.objects.get(id=self.kwargs["pk"])
        lead.agent = agent
        lead.save()
        return super(AssignAgentView, self).form_valid(form)


class CategoryListView(LoginRequiredMixin, generic.ListView):
    template_name = "leads/category_list.html"
    context_object_name = "category_list"

    def get_context_data(self, **kwargs):
        context = super(CategoryListView, self).get_context_data(**kwargs)
        user = self.request.user
        
        if user.is_organisor:
            queryset = Viajes.objects.filter(organisation=user.userprofile)
        else:
            queryset= Viajes.objects.filter(organisation=user.agent.organisation)

        context.update({
            "unnassigned_lead_count" : queryset.filter(category__isnull=True).count()
        })

        return context

    def get_queryset(self):
        # get the current user
        user = self.request.user      
        # initial queryset for the entire organisation (i.e. the agent or the organisor)
        if user.is_organisor:
            #query all the categories for certain organisation from the *organisation*
            queryset = Category.objects.filter(organisation=user.userprofile)
        else:
            #query all the categories for certain organisation from the *category* (note how the category and the organisation are linked: an organisation has leads under certain category)
            queryset= Category.objects.filter(organisation=user.agent.organisation)
        return queryset


class CategoryDetailView(LoginRequiredMixin, generic.DetailView):
    template_name = 'leads/category_detail.html'
    context_object_name = "category"

    def get_context_data(self, **kwargs):
        context = super(CategoryDetailView, self).get_context_data(**kwargs)
        
        # recall we are using a 'detail view', which means we are working with a specific instance of an object, in this case a category, we use the get_object method
        # in this class to fetch that object and use it to filter the leads that are in that category
        leads = Viajes.objects.filter(category=self.get_object()).all()       # NOTE: not sure if have to add '.all'
        
        #other way to do the latter is by doing a 'reverse lookup': from the 'Leads' table, using the 'related_name' attribute in that model, 
        # take all the leads that are in a category i.e. ->
        #leads = self.get_object().leads.all()
        
        context.update({
            "leads" : leads
        })

        return context

    def get_queryset(self):
        # get the current user
        user = self.request.user      
        # initial queryset for the entire organisation (i.e. the agent or the organisor)
        if user.is_organisor:
            #query all the categories for certain organisation from the *organisation*
            queryset = Category.objects.filter(organisation=user.userprofile)
        else:
            #query all the categories for certain organisation from the *category* (note how the category and the organisation are linked: an organisation has leads under certain category)
            queryset= Category.objects.filter(organisation=user.agent.organisation)
        return queryset


class LeadCategoryUpdateView(LoginRequiredMixin, generic.UpdateView):
    template_name = "leads/lead_category_update.html"
    form_class = LeadCategoryUpdateForm

    def get_queryset(self):
        user = self.request.user      
        if user.is_organisor:
            # initial queryset for the entire organisation
            queryset = Viajes.objects.filter(organisation=user.userprofile)      
        else:
            # in case an agent is the user, filter the leads that belong to them 
            queryset= Viajes.objects.filter(organisation=user.agent.organisation)
            queryset = queryset.filter(agent__user == self.request.user)
        return queryset  

    def get_success_url(self):
        #use the kwargs attribute in the reverse method to pass parameters to the url
        return reverse("leads:lead-detail", kwargs={ "pk": self.get_object().id })


class InicioViajeView(LoginRequiredMixin, generic.DetailView):
    template_name = 'leads/recoleccion_completada.html'
    queryset = Viajes.objects.all()
    
    
    context_object_name = 'viaje'

    def get_queryset(self):
        queryset = Viajes.objects.all()
        #print(queryset)
        return queryset

    def get_context_data(self, **kwargs):
        context = super(InicioViajeView, self).get_context_data(**kwargs)
        queryset2 = Imagenes_viajes.objects.filter(flete=self.get_object().pk)
        queryset2 = queryset2.filter(categoria='Recoleccion')
        #print(queryset2.first())
        if queryset2.first() == None:
            queryset2 = None
        else:
            queryset2 = queryset2.first()
        context.update({
                "imagen": queryset2
            })
        return context


class FinViajeView(LoginRequiredMixin, generic.DetailView):
    template_name = 'leads/viaje_completado.html'
    queryset = Viajes.objects.all()
    context_object_name = 'viaje'

    def get_context_data(self, **kwargs):
        context = super(FinViajeView, self).get_context_data(**kwargs)
        queryset2 = Imagenes_viajes.objects.filter(flete=self.get_object().pk)
        queryset2 = queryset2.filter(categoria='Entrega')
        if queryset2.first() == None:
            queryset2 = None
        else:
            queryset2 = queryset2.first()

        context.update({
                "imagen": queryset2
            })
        return context

class AyudaView(LoginRequiredMixin, generic.CreateView):
    template_name = 'leads/ayuda.html'
    form_class = AyudaForm
    
    def get_queryset(self):
        #print(self.get_object())
        return Viajes.objects.filter(id=self.get_object().id)

    def get_success_url(self):
        return reverse("leads:lead-list", kwargs={ "pk": self.get_object().id })
    
    def get_initial(self):
        initial = super(AyudaView, self).get_initial()
        # update initial field defaults with custom set default values:
        initial['name'] = self.request.user
        initial['flete_id'] = self.kwargs["pk"]
        return initial

class AyudaGralView(generic.CreateView):
    template_name = 'leads/ayuda_gral.html'
    form_class = AyudaForm
    
    def get_success_url(self):
        return reverse("leads:lead-list")

class EnConstruccionView(generic.TemplateView):
    template_name = 'construccion.html' 


class CustomLoginView(LoginView):
    authentication_form = CustomAuthenticationForm