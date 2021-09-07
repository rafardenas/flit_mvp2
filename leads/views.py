from django.core.mail import message, send_mail
from django.db.models import query
from django.db.models.query_utils import Q 
from django.http.response import HttpResponseRedirect
from django.shortcuts import render, redirect, reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.views import generic
from .models import Lead, Agent, Category
from .forms import LeadForm, LeadModelForm, CustomUserCreationForm, AssignAgentForm, LeadCategoryUpdateForm
from agents.mixins import OrganisorandLoginRequiredMixin

# Create your views here.

class SignupView(generic.CreateView):
    template_name = 'registration/signup.html'
    form_class = CustomUserCreationForm
    
    def get_success_url(self):
        return reverse("login")


class LandingPageView(generic.TemplateView):
    template_name = 'landing.html'


def landing_page(request):
    return render(request, 'landing.html')

class LeadListView(LoginRequiredMixin, generic.ListView):
    template_name = "leads/lead_list.html"
    context_object_name = "leads"

    def get_queryset(self):
        # get the current user
        user = self.request.user      
        # initial queryset for the entire organisation (i.e. the agent or the organisor)
        if user.is_organisor:
            #query all the leads for certain organisation from the *organisation*
            queryset = Lead.objects.filter(organisation=user.userprofile, 
                    agent__isnull=False)      #if the user is organisor, it will have a userprofile, otherwise that user is an agent.
        else:
            #query all the leads for certain organisation from the *agent* (note how the agent and the organisation are linked: a user can be an agent, and an agent has an organisation)
            queryset= Lead.objects.filter(organisation=user.agent.organisation)
            #filter for the agent that is logged in. (agent__user is equivalent to: `agent.user` in flask)
            queryset = queryset.filter(agent__user = user   )
        return queryset

    def get_context_data(self, **kwargs):
        context = super(LeadListView, self).get_context_data(**kwargs)
        user = self.request.user 
        if user.is_organisor:
            queryset = Lead.objects.filter(organisation=user.userprofile, agent__isnull=True)
            context.update({
                "unassigned_leads": queryset
            })
        return context


def lead_list(request):
    leads = Lead.objects.all()
    context = {
        "leads": leads  
    }
    return render(request, "leads/lead_list.html", context=context)

class LeadDetailView(LoginRequiredMixin, generic.DetailView):
    template_name = "leads/lead_detail.html"
    queryset = Lead.objects.all()
    context_object_name = 'lead'

    def get_queryset(self):
        user = self.request.user      
        if user.is_organisor:
            queryset = Lead.objects.filter(organisation=user.userprofile)      
        else:
            queryset= Lead.objects.filter(organisation=user.agent.organisation)
            queryset = queryset.filter(agent__user == self.request.user)
        return queryset


def lead_detail(request, pk):
    lead = Lead.objects.get(id=pk)
    context = {
        "lead":lead
    }
    return render(request, "leads/lead_detail.html", context)

class LeadCreateView(OrganisorandLoginRequiredMixin, generic.CreateView):
    template_name = "leads/lead_create.html"
    form_class = LeadModelForm
    
    def get_success_url(self):
        return reverse("leads:lead-list")
    
    def form_valid(self, form):
        # send email
        send_mail(subject="Se ha creado un nuevo viaje", message="Entra a Flit para monitorear el progreso",
        from_email="test@test.com",
        recipient_list=["test2@test.com"])
        return super(LeadCreateView, self).form_valid(form)


def lead_create(request):
    form = LeadModelForm()
    if request.method == 'POST':
        form = LeadModelForm(request.POST)
        if form.is_valid():
            # abstracts all the code that we'd  normally write to fill and submit a form:
            ##########
            #first_name = form.cleaned_data['first_name']
            #last_name = form.cleaned_data['last_name']
            #age = form.cleaned_data['age']
            #agent = form.cleaned_data['agent']
            #creating a new lead
            #Lead.objects.create(first_name=first_name, last_name=last_name, age=age, agent=agent)
            ##########
            form.save()
            return redirect('/leads')
    context = {
        "form": form
    }
    return render(request, "leads/lead_create.html", context=context)


class LeadUpdateView(OrganisorandLoginRequiredMixin, generic.UpdateView):
    template_name = "leads/lead_update.html"
    form_class = LeadModelForm

    def get_queryset(self):
        user = self.request.user      
        return Lead.objects.filter(organisation=user.userprofile)      

    def get_success_url(self):
        return reverse("leads:lead-list")


def lead_update(request, pk):
    lead = Lead.objects.get(id=pk)
    form = LeadModelForm(instance=lead)           #pass the specific instance of the form we want to update
    if request.method == "POST":
        form = LeadModelForm(request.POST, instance=lead)
        if form.is_valid():
            form.save() #commit the changes to the db
            return redirect("/leads")
    context = {
        'form':form,
        'lead':lead
    }
    return render(request, "leads/lead_update.html", context=context)


class LeadDeleteView(OrganisorandLoginRequiredMixin, generic.DeleteView):
    template_name = "leads/lead_delete.html"
    
    def get_queryset(self):
        user = self.request.user      
        return Lead.objects.filter(organisation=user.userprofile)    

    def get_success_url(self):
        return reverse("leads:lead-list")


def lead_delete(request, pk):
    lead = Lead.objects.get(id=pk)
    lead.delete()       #delete the instance from the db
    return redirect("/leads")


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
        print(self.kwargs)
        agent = form.cleaned_data["agent"]
        lead = Lead.objects.get(id=self.kwargs["pk"])
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
            queryset = Lead.objects.filter(organisation=user.userprofile)
        else:
            queryset= Lead.objects.filter(organisation=user.agent.organisation)

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
        leads = Lead.objects.filter(category=self.get_object()).all()       # NOTE: not sure if have to add '.all'
        
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
            queryset = Lead.objects.filter(organisation=user.userprofile)      
        else:
            # in case an agent is the user, filter the leads that belong to them 
            queryset= Lead.objects.filter(organisation=user.agent.organisation)
            queryset = queryset.filter(agent__user == self.request.user)
        return queryset  

    def get_success_url(self):
        #use the kwargs attribute in the reverse method to pass parameters to the url
        return reverse("leads:lead-detail", kwargs={ "pk": self.get_object().id })



