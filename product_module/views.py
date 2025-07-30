from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.urls import reverse_lazy

from .models import Product
from .mixins import RoleRequiredMixin


class ProductListView(ListView):
    model = Product
    template_name = 'product/product_list.html'


class ProductCreateView(RoleRequiredMixin, CreateView):
    model = Product
    fields = '__all__'
    template_name = 'product/product_form.html'
    success_url = reverse_lazy('product_list')
    allowed_roles = ['manager', 'user']


class ProductUpdateView(RoleRequiredMixin, UpdateView):
    model = Product
    fields = '__all__'
    template_name = 'product/product_form.html'
    success_url = reverse_lazy('product_list')
    allowed_roles = ['manager', 'user']


class ProductDeleteView(RoleRequiredMixin, DeleteView):
    model = Product
    template_name = 'product/product_confirm_delete.html'
    success_url = reverse_lazy('product_list')
    allowed_roles = ['manager']
