from django.shortcuts import render
from .models import *
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  UpdateView)

# Create your views here.
class ProductListView(ListView):
    model = Product
    template_name = 'Product/list_product.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'products'
    ordering = ['type_product__name', 'name']
    paginate_by = 10  # Số lượng phân trang