from django.shortcuts import render
from abc import ABC
from .models import *
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  UpdateView)
from django.contrib.auth.mixins import (LoginRequiredMixin,
                                        PermissionRequiredMixin,
                                        UserPassesTestMixin)
from Warehouse.models import Warehouse

# Create your views here.
class ProductListView(ListView):
    model = Product
    template_name = 'Product/list_product.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'products'
    ordering = ['type_product__name', 'name'] # sort by 
    paginate_by = 10  # Số lượng phân trang


class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    fields = ['type_product', 'provider','name', 'calculationUnit', 'unit_cost', 'selling_price', 'origin']
    template_name = 'Product/product_form.html'

    # def add new product in wwarehouse with count = 0 
    def get_success_url(self):
        warehouse = Warehouse(product=self.object)
        warehouse.save()
        return self.object.get_absolute_url()


class ProductUpdateView(LoginRequiredMixin, UpdateView, ABC):
    model = Product
    success_url = '' 
    # why success_url is '' because of the url now is host/product/ ( you using it in app url)
    fields = ['type_product', 'name','calculationUnit', 'unit_cost', 'selling_price','origin']
    template_name = 'Product/product_form.html'


class ProductDeleteView(LoginRequiredMixin, DeleteView, ABC):
    model = Product
    success_url = ''
    template_name = 'Product/product_confirm_delete.html'


class ProductDetailView(DetailView):
    model = Product
    template_name = 'Product/product_detail.html'


def List_typeProduct(request, type_product):
    template = "Product/list_type_product.html"
    products = Product.objects.filter(type_product__name = type_product).order_by('name')
    context = {'products': products,
               }
    return render(request, template, context)
