from django.db import models
from django.urls import reverse    


class Product(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    creation_datetime = models.DateTimeField(auto_now_add=True)
    modification_datetime = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('product_detail', kwargs={'pk': self.pk})

    class Meta:
        ordering = ['name']

class Component(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    git_repo_url = models.URLField(blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="components")
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
