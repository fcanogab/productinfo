from django import forms
from django.forms import inlineformset_factory
from .models import Component, ComponentFeature, Activity, JiraTicket, Result, Document

class ComponentForm(forms.ModelForm):
    class Meta:
        model = Component
        fields = ['name', 'description', 'git_repo_url', 'software', 'engineering_contact', 'business_contact', 'jira_ticket_url', 'dev_preview_date', 'tech_preview_date', 'general_availability_date']
        widgets = {
            'dev_preview_date': forms.DateInput(attrs={'type': 'date'}),
            'tech_preview_date': forms.DateInput(attrs={'type': 'date'}),
            'general_availability_date': forms.DateInput(attrs={'type': 'date'}),
        }

class ComponentFeatureForm(forms.ModelForm):
    class Meta:
        model = ComponentFeature
        fields = ['feature', 'description', 'priority', 'status', 'jira_ticket_url']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }

# Inline formset to handle ComponentFeature inside Component form
ComponentFeatureFormSet = inlineformset_factory(
    Component,
    ComponentFeature,
    form=ComponentFeatureForm,
    fields=['feature', 'description', 'priority', 'status', 'jira_ticket_url'],
    extra=1,  # one empty form initially
    can_delete=True
)

JiraTicketFormSet = inlineformset_factory(
    Activity, JiraTicket,
    fields=['name', 'url'],
    extra=1, can_delete=True
)

ResultFormSet = inlineformset_factory(
    Activity, Result,
    fields=['name', 'url'],
    extra=1, can_delete=True
)

DocumentFormSet = inlineformset_factory(
    Activity, Document,
    fields=['name', 'url'],
    extra=1, can_delete=True
)

class ActivityForm(forms.ModelForm):
    class Meta:
        model = Activity
        fields = ['name', 'description', 'execution_start_date', 'execution_end_date', 'status', 'component_version', 'component']
        widgets = {
            'execution_start_date': forms.DateInput(attrs={'type': 'date'}),
            'execution_end_date': forms.DateInput(attrs={'type': 'date'}),
        }
