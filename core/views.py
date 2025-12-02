from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.shortcuts import redirect
from .models import Software, Component, Feature, Threat, ComponentFeature, Activity, Campaign, FeatureCategory, Standard, Requirement
from .forms import ComponentForm, JiraTicketFormSet, ResultFormSet, DocumentFormSet, ActivityForm, SoftwareForm, ComponentFeatureForm, ComponentFeatureDocumentFormSet


class SoftwareCreate(CreateView):
    model = Software
    form_class = SoftwareForm
    success_url = reverse_lazy('software_list')

class SoftwareDetail(DetailView):
    model = Software

class SoftwareList(ListView):
    model = Software

class SoftwareUpdate(UpdateView):
    model = Software
    form_class = SoftwareForm

class SoftwareDelete(DeleteView):
    model = Software

    success_url = reverse_lazy('software_list')


class ComponentCreate(CreateView):
    model = Component
    form_class = ComponentForm

    def get_initial(self):
        initial = super().get_initial()
        software_pk = self.kwargs.get('software_pk')
        if software_pk:
            initial['software'] = software_pk
        return initial

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

    def get_success_url(self):
        return reverse_lazy('component_detail', kwargs={'pk': self.object.pk})

class ComponentDelete(DeleteView):
    model = Component

    def get_success_url(self):
        return reverse_lazy('software_detail', kwargs={'pk': self.object.software.pk})


class FeatureCreate(CreateView):
    model = Feature
    fields = ['name', 'description', 'category']

    success_url = reverse_lazy('feature_list')

class FeatureList(ListView):
    model = Feature

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['featurecategory_list'] = FeatureCategory.objects.all()
        context['features_without_category'] = Feature.objects.filter(category__isnull=True)
        return context

class FeatureDetail(DetailView):
    model = Feature

class FeatureUpdate(UpdateView):
    model = Feature
    fields = ['name', 'description', 'category']

class FeatureDelete(DeleteView):
    model = Feature

    success_url = reverse_lazy('feature_list')


class FeatureCategoryCreate(CreateView):
    model = FeatureCategory
    fields = ['name', 'description']

    success_url = reverse_lazy('featurecategory_list')

class FeatureCategoryDetail(DetailView):
    model = FeatureCategory

class FeatureCategoryUpdate(UpdateView):
    model = FeatureCategory
    fields = ['name', 'description']

class FeatureCategoryDelete(DeleteView):
    model = FeatureCategory

    success_url = reverse_lazy('featurecategory_list')

class FeatureCategoryList(ListView):
    model = FeatureCategory


class ComponentFeatureCreate(CreateView):
    model = ComponentFeature
    form_class = ComponentFeatureForm

    def get_initial(self):
        initial = super().get_initial()
        component_pk = self.kwargs.get('component_pk')
        if component_pk:
            initial['component'] = component_pk
        return initial

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['document_formset'] = ComponentFeatureDocumentFormSet(self.request.POST, prefix='document')
        else:
            context['document_formset'] = ComponentFeatureDocumentFormSet(prefix='document')
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        document_formset = context['document_formset']
        self.object = form.save()
        selected_campaigns = form.cleaned_data.get('campaigns')
        if selected_campaigns is not None:
            self.object.campaigns.set(selected_campaigns)
        if document_formset.is_valid():
            document_formset.instance = self.object
            document_formset.save()
        return redirect(self.get_success_url())

    def get_success_url(self):
        return reverse_lazy('component_detail', kwargs={'pk': self.object.component.pk})


class ComponentFeatureUpdate(UpdateView):
    model = ComponentFeature
    form_class = ComponentFeatureForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['document_formset'] = ComponentFeatureDocumentFormSet(self.request.POST, instance=self.object, prefix='document')
        else:
            context['document_formset'] = ComponentFeatureDocumentFormSet(instance=self.object, prefix='document')
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        document_formset = context['document_formset']
        self.object = form.save()
        selected_campaigns = form.cleaned_data.get('campaigns')
        if selected_campaigns is not None:
            self.object.campaigns.set(selected_campaigns)
        if document_formset.is_valid():
            document_formset.instance = self.object
            document_formset.save()
        return redirect(self.get_success_url())

    def get_success_url(self):
        return reverse_lazy('component_detail', kwargs={'pk': self.object.component.pk})


class ComponentFeatureDelete(DeleteView):
    model = ComponentFeature

    def get_success_url(self):
        component = self.object.component
        return component.get_absolute_url()


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


class ActivityCreate(CreateView):
    model = Activity
    form_class = ActivityForm

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
            form.save_m2m() if hasattr(form, 'save_m2m') else None
            # Save selected existing campaigns only
            selected_campaigns = form.cleaned_data.get('campaigns')
            if selected_campaigns is not None:
                self.object.campaigns.set(selected_campaigns)
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
    form_class = ActivityForm

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
            form.save_m2m() if hasattr(form, 'save_m2m') else None
            # Save selected existing campaigns only
            selected_campaigns = form.cleaned_data.get('campaigns')
            if selected_campaigns is not None:
                self.object.campaigns.set(selected_campaigns)
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


class CampaignCreate(CreateView):
    model = Campaign
    fields = ['name', 'description', 'status', 'due_date', 'jira_ticket_url']

    success_url = reverse_lazy('campaign_list')

class CampaignDetail(DetailView):
    model = Campaign

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pending_activities'] = self.object.activities.filter(status__in=[1, 2])
        context['todo_activities'] = self.object.activities.filter(status=1)
        context['in_progress_activities'] = self.object.activities.filter(status=2)
        context['done_activities'] = self.object.activities.filter(status=3)
        context['pending_component_features'] = self.object.component_features.filter(status__in=[1, 2])
        context['todo_component_features'] = self.object.component_features.filter(status=1)
        context['in_progress_component_features'] = self.object.component_features.filter(status=2)
        context['done_component_features'] = self.object.component_features.filter(status=3)
        context['pending_total'] = context['pending_activities'].count() + context['pending_component_features'].count()
        context['todo_total'] = context['todo_activities'].count() + context['todo_component_features'].count()
        context['in_progress_total'] = context['in_progress_activities'].count() + context['in_progress_component_features'].count()
        context['done_total'] = context['done_activities'].count() + context['done_component_features'].count()
        return context

class CampaignList(ListView):
    model = Campaign

class CampaignUpdate(UpdateView):
    model = Campaign
    fields = ['name', 'description', 'status', 'due_date', 'jira_ticket_url']

class CampaignDelete(DeleteView):
    model = Campaign
    success_url = reverse_lazy('campaign_list')


class StandardCreate(CreateView):
    model = Standard
    fields = ['name', 'code', 'description']

    success_url = reverse_lazy('standard_list')

class StandardDetail(DetailView):
    model = Standard

class StandardUpdate(UpdateView):
    model = Standard
    fields = ['name', 'code', 'description']

class StandardDelete(DeleteView):
    model = Standard
    success_url = reverse_lazy('standard_list')

class StandardList(ListView):
    model = Standard


class RequirementCreate(CreateView):
    model = Requirement
    fields = ['definition', 'name', 'code', 'standard']

    def get_initial(self):
        initial = super().get_initial()
        standard_pk = self.kwargs.get('standard_pk')
        if standard_pk:
            initial['standard'] = standard_pk
        return initial

    def get_success_url(self):
        return reverse_lazy('standard_detail', kwargs={'pk': self.object.standard.pk})

class RequirementDetail(DetailView):
    model = Requirement

class RequirementUpdate(UpdateView):
    model = Requirement
    fields = ['definition', 'name', 'code', 'standard']

    def get_success_url(self):
        return reverse_lazy('standard_detail', kwargs={'pk': self.object.standard.pk})

class RequirementDelete(DeleteView):
    model = Requirement
    
    def get_success_url(self):
        return reverse_lazy('standard_detail', kwargs={'pk': self.object.standard.pk})

class RequirementList(ListView):
    model = Requirement
