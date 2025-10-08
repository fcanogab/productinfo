from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Product


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
