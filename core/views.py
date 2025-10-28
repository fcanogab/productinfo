from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.shortcuts import redirect
from .models import Software, Component, Feature, Threat, ComponentFeature, Activity
from .forms import ComponentForm, ComponentFeatureFormSet, JiraTicketFormSet, ResultFormSet, DocumentFormSet


class SoftwareCreate(CreateView):
    model = Software
    fields = ['name', 'description']

    success_url = reverse_lazy('software_list')
  
class SoftwareDetail(DetailView):
    model = Software

class SoftwareList(ListView):
    model = Software

class SoftwareUpdate(UpdateView):
    model = Software
    fields = ['name', 'description']

class SoftwareDelete(DeleteView):
    model = Software

    success_url = reverse_lazy('software_list')


class ComponentCreate(CreateView):
    model = Component
    form_class = ComponentForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['formset'] = ComponentFeatureFormSet(self.request.POST)
        else:
            context['formset'] = ComponentFeatureFormSet()
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context['formset']
        self.object = form.save()
        if formset.is_valid():
            formset.instance = self.object
            formset.save()
        return redirect(self.get_success_url())

    def form_invalid(self, form):
        context = self.get_context_data()
        context['form'] = form
        return self.render_to_response(context)

    def get_success_url(self):
        return reverse_lazy('component_detail', kwargs={'pk': self.object.pk})
  
class ComponentDetail(DetailView):
    model = Component

class ComponentUpdate(UpdateView):
    model = Component
    form_class = ComponentForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['formset'] = ComponentFeatureFormSet(self.request.POST, instance=self.object)
        else:
            context['formset'] = ComponentFeatureFormSet(instance=self.object)
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context['formset']
        print(formset.errors)
        self.object = form.save()
        if formset.is_valid():
            formset.instance = self.object
            formset.save()
        return redirect(self.get_success_url())

    def get_success_url(self):
        return reverse_lazy('component_detail', kwargs={'pk': self.object.pk})

class ComponentDelete(DeleteView):
    model = Component

    def get_success_url(self):
        return reverse_lazy('software_detail', kwargs={'pk': self.object.software.pk})


class FeatureCreate(CreateView):
    model = Feature
    fields = ['name', 'description']

    success_url = reverse_lazy('feature_list')

class FeatureList(ListView):
    model = Feature

class FeatureDetail(DetailView):
    model = Feature

class FeatureUpdate(UpdateView):
    model = Feature
    fields = ['name', 'description']

class FeatureDelete(DeleteView):
    model = Feature

    success_url = reverse_lazy('feature_list')


class ThreatCreate(CreateView):
    model = Threat
    fields = ['name', 'description']

    success_url = reverse_lazy('threat_list')

class ThreatList(ListView):
    model = Threat

class ThreatDetail(DetailView):
    model = Threat

class ThreatUpdate(UpdateView):
    model = Threat
    fields = ['name', 'description']

class ThreatDelete(DeleteView):
    model = Threat

    success_url = reverse_lazy('threat_list')


class ComponentFeatureDelete(DeleteView):
    model = ComponentFeature

    def get_success_url(self):
        component = self.object.component
        return component.get_absolute_url()


class ActivityCreate(CreateView):
    model = Activity
    fields = ['name', 'description', 'execution_start_date', 'execution_end_date', 'status', 'component_version', 'component']

    def get_initial(self):
        initial = super().get_initial()
        component_pk = self.kwargs.get('component_pk')
        if component_pk:
            initial['component'] = component_pk
        return initial

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['jira_formset'] = JiraTicketFormSet(self.request.POST, prefix='jira')
            context['result_formset'] = ResultFormSet(self.request.POST, prefix='result')
            context['document_formset'] = DocumentFormSet(self.request.POST, prefix='document')
        else:
            context['jira_formset'] = JiraTicketFormSet(prefix='jira')
            context['result_formset'] = ResultFormSet(prefix='result')
            context['document_formset'] = DocumentFormSet(prefix='document')
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        jira_formset = context['jira_formset']
        result_formset = context['result_formset']
        document_formset = context['document_formset']
        self.object = form.save()
        if (jira_formset.is_valid() and result_formset.is_valid() and document_formset.is_valid()):
            jira_formset.instance = self.object
            result_formset.instance = self.object
            document_formset.instance = self.object
            jira_formset.save()
            result_formset.save()
            document_formset.save()
            return redirect(self.get_success_url())
        else:
            return self.form_invalid(form)

    def get_success_url(self):
        return reverse_lazy('component_detail', kwargs={'pk': self.object.component.pk})

class ActivityList(ListView):
    model = Activity

class ActivityDetail(DetailView):
    model = Activity

class ActivityUpdate(UpdateView):
    model = Activity
    fields = ['name', 'description', 'execution_start_date', 'execution_end_date', 'status', 'component_version', 'component']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['jira_formset'] = JiraTicketFormSet(self.request.POST, instance=self.object, prefix='jira')
            context['result_formset'] = ResultFormSet(self.request.POST, instance=self.object, prefix='result')
            context['document_formset'] = DocumentFormSet(self.request.POST, instance=self.object, prefix='document')
        else:
            context['jira_formset'] = JiraTicketFormSet(instance=self.object, prefix='jira')
            context['result_formset'] = ResultFormSet(instance=self.object, prefix='result')
            context['document_formset'] = DocumentFormSet(instance=self.object, prefix='document')
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        jira_formset = context['jira_formset']
        result_formset = context['result_formset']
        document_formset = context['document_formset']
        self.object = form.save()
        if (jira_formset.is_valid() and result_formset.is_valid() and document_formset.is_valid()):
            jira_formset.instance = self.object
            result_formset.instance = self.object
            document_formset.instance = self.object
            jira_formset.save()
            result_formset.save()
            document_formset.save()
            return redirect(self.get_success_url())
        else:
            return self.form_invalid(form)

    def get_success_url(self):
        return reverse_lazy('component_detail', kwargs={'pk': self.object.component.pk})

class ActivityDelete(DeleteView):
    model = Activity

    def get_success_url(self):
        return reverse_lazy('component_detail', kwargs={'pk': self.object.component.pk})
