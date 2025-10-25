from django.db import models
from django.urls import reverse    


class Software(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    creation_datetime = models.DateTimeField(auto_now_add=True)
    modification_datetime = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('software_detail', kwargs={'pk': self.pk})

    class Meta:
        ordering = ['name']
        verbose_name_plural = 'software'


class Component(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    git_repo_url = models.URLField(blank=True)
    software = models.ForeignKey('Software', on_delete=models.CASCADE, related_name="components")
    engineering_contact = models.CharField(max_length=100, blank=True)
    business_contact = models.CharField(max_length=100, blank=True)
    jira_ticket_url = models.URLField(blank=True)
    dev_preview_date = models.DateField(null=True, blank=True)
    tech_preview_date = models.DateField(null=True, blank=True)
    general_availability_date = models.DateField(null=True, blank=True)
    creation_datetime = models.DateTimeField(auto_now_add=True)
    modification_datetime = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('component_detail', kwargs={'pk': self.pk})

    class Meta:
        ordering = ['name']


class Feature(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    components = models.ManyToManyField('Component', through="ComponentFeature", related_name="features")
    creation_datetime = models.DateTimeField(auto_now_add=True)
    modification_datetime = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('feature_detail', kwargs={'pk': self.pk})

    class Meta:
        ordering = ['name']


class Threat(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    creation_datetime = models.DateTimeField(auto_now_add=True)
    modification_datetime = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('threat_detail', kwargs={'pk': self.pk})

    class Meta:
        ordering = ['name']


class ComponentFeature(models.Model):
    PRIORITY_CHOICES = [
        (1, 'Low'),
        (2, 'Medium'),
        (3, 'High'),
    ]

    LOW = 1
    MEDIUM = 2
    HIGH = 3

    STATUS_CHOICES = [
        (1, 'To Do'),
        (2, 'In Progress'),
        (3, 'Done'),
    ]

    TO_DO = 1
    IN_PROGRESS = 2
    DONE = 3

    description = models.TextField(blank=True)
    priority = models.IntegerField(choices=PRIORITY_CHOICES, default=MEDIUM)
    status = models.IntegerField(choices=STATUS_CHOICES, default=TO_DO)
    component = models.ForeignKey('Component', on_delete=models.CASCADE, related_name="component_features")
    feature = models.ForeignKey('Feature', on_delete=models.CASCADE, related_name="component_features")
    jira_ticket_url = models.URLField(blank=True)
    creation_datetime = models.DateTimeField(auto_now_add=True)
    modification_datetime = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.component.name} - {self.feature.name}"
    
    class Meta:
        ordering = ['component__name', 'feature__name']
        unique_together = ['component', 'feature']


class Activity(models.Model):
    STATUS_CHOICES = [
        (1, 'To Do'),
        (2, 'In Progress'),
        (3, 'Done'),
    ]

    TO_DO = 1
    IN_PROGRESS = 2
    DONE = 3
    
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    execution_start_date = models.DateField(null=True, blank=True)
    execution_end_date = models.DateField(null=True, blank=True)
    status = models.IntegerField(choices=STATUS_CHOICES, default=TO_DO)
    component_version = models.CharField(max_length=100, blank=True)
    component = models.ForeignKey('Component', on_delete=models.CASCADE, related_name="activities")
    creation_datetime = models.DateTimeField(auto_now_add=True)
    modification_datetime = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['name']
        verbose_name_plural = 'activities'
        unique_together = ['name', 'component']
