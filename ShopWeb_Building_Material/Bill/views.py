from django.shortcuts import render
from .models import *
from django.contrib.auth.mixins import (LoginRequiredMixin,
                                        PermissionRequiredMixin,
                                        UserPassesTestMixin)
from django.contrib.auth.models import User
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  UpdateView)
from abc import ABC
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render


# Create your views here.

# list view
class InputBillListView(PermissionRequiredMixin, ListView):
    # permission_required = 'vatlieu.view_inputbill'
    model = InputBill
    template_name = 'vatlieu/list/list_input_bill.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'input_bills'
    ordering = ['-input_date']
    paginate_by = 10  # Số lượng phân trang

    def handle_no_permission(self):
            return redirect('Webshop:home')


class OutputBillListView(PermissionRequiredMixin, ListView):
    # permission_required = 'vatlieu.view_outputbill'
    model = OutputBill
    template_name = 'vatlieu/list/list_output_bill.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'output_bills'
    ordering = ['-output_date']
    paginate_by = 10  # Số lượng phân trang

    def handle_no_permission(self):
        return redirect('Webshop:home')


class UserInputBillListView(ListView):
    model = InputBill
    template_name = 'vatlieu/staff/staff_input_bill.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'input_bills'  # using in template
    ordering = ['-input_date']
    paginate_by = 10  # Số lượng phân trang

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return InputBill.objects.filter(staff=user).order_by('-input_date')


class UserOutputBillListView(ListView):
    model = OutputBill
    template_name = 'vatlieu/staff/staff_output_bill.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'output_bills'  # using in template
    ordering = ['-output_date']
    paginate_by = 5  # Số lượng phân trang

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return OutputBill.objects.filter(staff=user).order_by('-output_date')

