from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Product, Component


class ProductCreate(CreateView):
    model = Product
    fields = ['name', 'description']

    success_url = reverse_lazy('product_list')
  
class ProductDetail(DetailView):
    model = Product

class ProductList(ListView):
    model = Product

class ProductUpdate(UpdateView):
    model = Product
    fields = ['name', 'description']

class ProductDelete(DeleteView):
    model = Product

    success_url = reverse_lazy('product_list')

class ComponentCreate(CreateView):
    model = Component
    fields = ['name', 'description', 'git_repo_url', 'product']

    def get_success_url(self):
        return reverse_lazy('product_detail', kwargs={'pk': self.object.product.pk})
  
class ComponentDetail(DetailView):
    model = Component

class ComponentUpdate(UpdateView):
    model = Component
    fields = ['name', 'description', 'git_repo_url', 'product']

    def get_success_url(self):
        return reverse_lazy('product_detail', kwargs={'pk': self.object.product.pk})

class ComponentDelete(DeleteView):
    model = Component

    success_url = reverse_lazy('component_detail')
