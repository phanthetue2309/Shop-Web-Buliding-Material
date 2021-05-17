from django.shortcuts import render
from .models import *
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  UpdateView)

# Create your views here.
class CustomerListView(ListView):
    model = Customer
    template_name = 'Customer/list_customer.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'customers'
    ordering = ['-id']
    paginate_by = 10  # Số lượng phân trang


class ProviderListView(ListView):
    model = Provider
    template_name = 'Provider/list_provider.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'providers'
    ordering = ['-id']
    paginate_by = 10  # Số lượng phân trang