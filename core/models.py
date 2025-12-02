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
    psrd_contact = models.CharField(max_length=100, blank=True)
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
    category = models.ForeignKey('FeatureCategory', on_delete=models.CASCADE, related_name="features", blank=True, null=True)
    creation_datetime = models.DateTimeField(auto_now_add=True)
    modification_datetime = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('feature_detail', kwargs={'pk': self.pk})

    class Meta:
        ordering = ['name']

class FeatureCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    creation_datetime = models.DateTimeField(auto_now_add=True)
    modification_datetime = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

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
    estimated_completion_date = models.DateField(null=True, blank=True)
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


class ComponentActivity(models.Model):
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE, related_name='component_activities')
    estimated_completion_date = models.DateField(null=True, blank=True)
    execution_start_date = models.DateField(null=True, blank=True)
    execution_end_date = models.DateField(null=True, blank=True)
    status = models.IntegerField(choices=Activity.STATUS_CHOICES, default=Activity.TO_DO)
    component_version = models.CharField(max_length=100, blank=True)
    component = models.ForeignKey('Component', on_delete=models.CASCADE, related_name="component_activities")
    creation_datetime = models.DateTimeField(auto_now_add=True)
    modification_datetime = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.component.name} - {self.activity.name}"

    class Meta:
        ordering = ['component__name', 'activity__name']
        unique_together = ['component', 'activity']


class Link(models.Model):
    url = models.URLField()
    name = models.CharField(max_length=255)
    creation_datetime = models.DateTimeField(auto_now_add=True)
    modification_datetime = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']

class JiraTicket(Link):
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE, related_name="jira_tickets", blank=True, null=True)

class Result(Link):
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE, related_name="results", blank=True, null=True)

class Document(Link):
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE, related_name="documents", blank=True, null=True)
    component_feature = models.ForeignKey(ComponentFeature, on_delete=models.CASCADE, related_name="documents", blank=True, null=True)

class Campaign(models.Model):
    STATUS_CHOICES = [
        (1, 'To Do'),
        (2, 'In Progress'),
        (3, 'Done'),
    ]

    TO_DO = 1
    IN_PROGRESS = 2
    DONE = 3

    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    status = models.IntegerField(choices=STATUS_CHOICES, default=TO_DO)
    due_date = models.DateField(null=True, blank=True)
    jira_ticket_url = models.URLField(blank=True)
    activities = models.ManyToManyField('Activity', through="ActivityCampaign", related_name="campaigns")
    component_features = models.ManyToManyField('ComponentFeature', through="ComponentFeatureCampaign", related_name="campaigns")
    creation_datetime = models.DateTimeField(auto_now_add=True)
    modification_datetime = models.DateTimeField(auto_now=True)

    def get_absolute_url(self):
        return reverse('campaign_detail', kwargs={'pk': self.pk})

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']

class ActivityCampaign(models.Model):
    activity = models.ForeignKey('Activity', on_delete=models.CASCADE)
    campaign = models.ForeignKey('Campaign', on_delete=models.CASCADE)
    creation_datetime = models.DateTimeField(auto_now_add=True)
    modification_datetime = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.activity.name} - {self.campaign.name}"

    class Meta:
        ordering = ['activity__name', 'campaign__name']
        unique_together = ['activity', 'campaign']

class ComponentFeatureCampaign(models.Model):
    component_feature = models.ForeignKey('ComponentFeature', on_delete=models.CASCADE)
    campaign = models.ForeignKey('Campaign', on_delete=models.CASCADE)
    creation_datetime = models.DateTimeField(auto_now_add=True)
    modification_datetime = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.component_feature.feature.name} - {self.campaign.name}"

    class Meta:
        ordering = ['component_feature__feature__name', 'campaign__name']
        unique_together = ['component_feature', 'campaign']

class Standard(models.Model):
    name = models.CharField(max_length=300, unique=True)
    code = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    components = models.ManyToManyField('Component', through="ComponentStandard", related_name="standards")
    creation_datetime = models.DateTimeField(auto_now_add=True)
    modification_datetime = models.DateTimeField(auto_now=True)

    def get_absolute_url(self):
        return reverse('standard_detail', kwargs={'pk': self.pk})

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']

class ComponentStandard(models.Model):
    component = models.ForeignKey('Component', on_delete=models.CASCADE)
    standard = models.ForeignKey('Standard', on_delete=models.CASCADE)
    creation_datetime = models.DateTimeField(auto_now_add=True)
    modification_datetime = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.component.name} - {self.standard.name}"

    class Meta:
        ordering = ['component__name', 'standard__name']
        unique_together = ['component', 'standard']

class Requirement(models.Model):
    definition = models.TextField()
    name = models.CharField(max_length=300, blank=True)
    code = models.CharField(max_length=100, blank=True)
    standard = models.ForeignKey('Standard', on_delete=models.CASCADE, related_name="requirements")
    features = models.ManyToManyField('Feature', through="FeatureRequirement", related_name="requirements")
    activities = models.ManyToManyField('Activity', through="ActivityRequirement", related_name="requirements")
    creation_datetime = models.DateTimeField(auto_now_add=True)
    modification_datetime = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.standard.name} - {self.definition}"
    
    def get_absolute_url(self):
        return reverse('requirement_detail', kwargs={'pk': self.pk})

    class Meta:
        ordering = ['creation_datetime']
        unique_together = ['standard', 'definition']

class FeatureRequirement(models.Model):
    feature = models.ForeignKey('Feature', on_delete=models.CASCADE)
    requirement = models.ForeignKey('Requirement', on_delete=models.CASCADE)
    creation_datetime = models.DateTimeField(auto_now_add=True)
    modification_datetime = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.feature.name} - {self.requirement.name}"

    class Meta:
        ordering = ['feature__name', 'requirement__name']
        unique_together = ['feature', 'requirement']

class ActivityRequirement(models.Model):
    activity = models.ForeignKey('Activity', on_delete=models.CASCADE)
    requirement = models.ForeignKey('Requirement', on_delete=models.CASCADE)
    creation_datetime = models.DateTimeField(auto_now_add=True)
    modification_datetime = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.activity.name} - {self.requirement.name}"

    class Meta:
        ordering = ['activity__name', 'requirement__name']
        unique_together = ['activity', 'requirement']
