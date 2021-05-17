from django.shortcuts import render
from .models import *
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  UpdateView)
# Create your views here.
class WarehouseListView(ListView):
    model = Warehouse
    template_name = 'Warehouse/warehouse.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'warehouse'
    ordering = ['product__typeproduct__name', 'product__name']
    paginate_by = 10  # Số lượng phân trang