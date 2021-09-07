import random
from django.views import generic
from django.core.mail import message, send_mail
from .mixins import OrganisorandLoginRequiredMixin
from django.shortcuts import reverse
from leads.models import Agent
from .forms import AgentModelForm



class AgentListView(OrganisorandLoginRequiredMixin, generic.ListView):
    template_name = "agents/agent-list.html"
    
    #query to see only the agents the active user had created
    def get_queryset(self):
        organisation = self.request.user.userprofile
        return Agent.objects.filter(organisation=organisation)

class AgentCreateView(OrganisorandLoginRequiredMixin, generic.CreateView):
    template_name = "agents/agent-create.html"
    form_class = AgentModelForm

    def get_success_url(self):
        return reverse('agents:agent-list')
    
    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_agent = True
        user.is_organisor = False
        user.set_password(f"{random.randint(0,1e6)}")
        user.save()
        Agent.objects.create(user=user, organisation=self.request.user.userprofile)
        send_mail(
            subject = 'Estas invitado a Flit', 
            message = 'Estas invitado a Flit',
            from_email = "admin@test.com", 
            recipient_list = [user.email]
        )
        return super(AgentCreateView, self).form_valid(form)

class AgentDetailView(OrganisorandLoginRequiredMixin, generic.DetailView):
    template_name = 'agents/agent-detail.html'
    context_object_name = 'agent'
    
    def get_queryset(self):
        organisation = self.request.user.userprofile
        return Agent.objects.filter(organisation=organisation)

class AgentUpdateView(OrganisorandLoginRequiredMixin, generic.UpdateView):
    template_name = "agents/agent-update.html"
    form_class = AgentModelForm
    queryset = Agent.objects.all()
    
    def get_success_url(self):
        return reverse("agents:agent-list")

class AgentDeleteView(OrganisorandLoginRequiredMixin, generic.DeleteView):
    template_name = 'agents/agent-delete.html'
    context_object_name = 'agent'
    
    def get_queryset(self):
        organisation = self.request.user.userprofile
        return Agent.objects.filter(organisation=organisation)

    def get_success_url(self):
        return reverse("agents:agent-list")
