from django.shortcuts import render
from abc import ABC
from .models import *
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  UpdateView)
from django.contrib.auth.mixins import (LoginRequiredMixin,
                                        PermissionRequiredMixin,
                                        UserPassesTestMixin)

# Create your views here.
# Customer Views
class CustomerListView(ListView):
    model = Customer
    template_name = 'Customer/list_customer.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'customers'
    ordering = ['-id']
    paginate_by = 10  # Số lượng phân trang

success_url_customer = "people/customer"

class CustomerCreateView(LoginRequiredMixin, CreateView):
    model = Customer    
    fields = ['name', 'address', 'phone_number', 'discription']
    template_name = 'Customer/customer_form.html'
    success_url = success_url_customer


class CustomerUpdateView(LoginRequiredMixin, UpdateView, ABC):
    model = Customer
    success_url = success_url_customer
    fields = ['name', 'address', 'phone_number']
    template_name = 'Customer/customer_form.html'


class CustomerDeleteView(LoginRequiredMixin, DeleteView, ABC):
    model = Customer
    success_url = success_url_customer
    template_name = 'Customer/customer_confirm_delete.html'


class CustomerDetailView(DetailView):
    model = Customer
    template_name = 'Customer/customer_detail.html'

# Provider Views
class ProviderListView(ListView):
    model = Provider
    template_name = 'Provider/list_provider.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'providers'
    ordering = ['-id']
    paginate_by = 10  # Số lượng phân trang

success_url_provider = ""
class ProviderCreateView(LoginRequiredMixin, CreateView):
    model = Provider
    fields = ['name', 'address', 'phone_number','website','email']
    template_name = 'Provider/provider_form.html'
    success_url = success_url_provider


class ProviderUpdateView(LoginRequiredMixin, UpdateView, ABC):
    model = Provider
    success_url = success_url_provider
    fields = ['name', 'address', 'phone_number','website','email']
    template_name = 'Provider/provider_form.html'


class ProviderDeleteView(LoginRequiredMixin, DeleteView, ABC):
    model = Provider
    success_url = success_url_provider
    template_name = 'Provider/provider_confirm_delete.html'


class ProviderDetailView(DetailView):
    model = Provider
    template_name = 'Provider/provider_detail.html'