from django import forms
from django.forms import inlineformset_factory
from .models import Component, ComponentFeature

class ComponentForm(forms.ModelForm):
    class Meta:
        model = Component
        fields = ['name', 'description', 'git_repo_url', 'software', 'engineering_contact', 'business_contact']

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
