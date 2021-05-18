from typing import List
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
from django.forms import inlineformset_factory
# Create your views here.

# INPUT
class InputBillListView(PermissionRequiredMixin, ListView):
    permission_required = 'Bill.view_inputbill'
    model = InputBill
    template_name = 'Input_Bill/list_input_bill.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'input_bills'
    ordering = ['-input_date']
    paginate_by = 10  # Số lượng phân trang

    def handle_no_permission(self):
            return redirect('Webshop:home')


class InputBillCreateView(LoginRequiredMixin, CreateView):
    model = InputBill
    fields = ['provider', 'input_date', 'flag']  # field must contains in models
    template_name = 'Input_bill/input_bill_form.html'

    def form_valid(self, form):
        form.instance.staff = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return self.object.get_absolute_url()


class InputBillUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView, ABC):
    model = InputBill
    fields = ['provider', 'input_date', 'flag']
    template_name = 'Input_Bill/input_bill_form.html'
    success_url = 'input'

    def form_valid(self, form):
        form.instance.staff = self.request.user
        return super().form_valid(form)

    def test_func(self):
        input_bill = self.get_object()
        if self.request.user == input_bill.staff:
            return True
        return False


class InputBillDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView, ABC):
    model = InputBill
    success_url = 'input'
    template_name = 'Input_Billinput_bill_confirm_delete.html'

    def test_func(self):
        input_bill = self.get_object()
        if self.request.user == input_bill.staff:
            return True
        return False


class DetailInputUpdateView(LoginRequiredMixin, UpdateView, ABC):
    model = DetailInputBill
    fields = ['product', 'count']
    template_name = 'Input_Bill/detail_input_bill/detail_bill_update.html'
    old_data = []

    def get_context_data(self, **kwargs):
        # pk = self.kwargs.get(self.pk_url_kwarg)  # use to get pk of objects
        context = super().get_context_data(**kwargs)
        context['product'] = self.object.product  # get data in the form when log in
        context['count'] = self.object.count
        self.old_data.clear()  
        # keep old data
        self.old_data.append(context['product'])
        self.old_data.append(context['count'])
        return context

    def get_success_url(self):
        print(self.old_data)
        if self.old_data[0].name == self.object.product.name:
            warehouse = Warehouse.objects.get(product__name=self.object.product.name)
            warehouse.count -= self.old_data[1]
            warehouse.count += self.object.count
            warehouse.save()
        else:
            warehouse = Warehouse.objects.get(product__name=self.old_data[0].name)
            warehouse.count -= self.old_data[1]
            warehouse.save()
            warehouse_new = Warehouse.objects.get(product__name=self.object.product.name)
            warehouse_new.count += self.object.count
            warehouse_new.save()
        return self.object.get_update_return()


class DetailInputDeleteView(LoginRequiredMixin, DeleteView, ABC):
    model = DetailInputBill
    template_name = 'vatlieu/input_bill/detail_input_bill/detail_bill_delete.html'

    def get_success_url(self):
        return self.object.get_update_return()


class UserInputBillListView(ListView):
    model = InputBill
    template_name = 'Input_Bill/staff_input_bill.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'input_bills'  # using in template
    ordering = ['-input_date']
    paginate_by = 10  # Số lượng phân trang

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return InputBill.objects.filter(staff=user).order_by('-input_date')


# create detail input bill
@login_required(login_url='login')
def create_detail_inputbill(request, pk):
    detail_input_bill_formset = inlineformset_factory(InputBill, DetailInputBill,
                                                      fields=('product', 'count'), extra=10)
    # why use input_bill and detail_input because it has been created before now we need to
    # insert more than product in the input bill so we choice inlineformset like that
    input_bill = InputBill.objects.get(id=pk)
    formset = detail_input_bill_formset(queryset=DetailInputBill.objects.none(), instance=input_bill)
    if request.method == 'POST':
        formset = detail_input_bill_formset(request.POST, instance=input_bill)
        if formset.is_valid():
            for f in formset:
                # it run all for even not data in that so you have to make try catch to
                # remove the data not has enough data you need
                cd = f.cleaned_data
                product_name = cd.get('product')
                count = cd.get('count')
                # update data in warehouse
                try:
                    warehouse = Warehouse.objects.get(product__name=product_name)
                except Warehouse.DoesNotExist:
                    warehouse = None
                if warehouse is not None:
                    print(warehouse.product)
                    warehouse.count += count
                    warehouse.save()

            formset.save()
            return redirect('/bill/input_bill')

    context = {'form': formset}
    return render(request, 'Input_Bill/detail_input_bill/input_bill_detail_form.html', context)


# detail of bill
def all_detail_input_bill(request, pk):
    sum_price = 0
    status = "UnDeal"
    input_bill = InputBill.objects.get(id=pk)
    if input_bill.flag == 1:
        status = "Deal"
    input_bill_detail = DetailInputBill.objects.filter(input_bill__id=pk)
    for bill in input_bill_detail:
        bill.price = bill.product.unit_cost * bill.count
        sum_price += bill.price
    context = {
        'input_bill': input_bill,
        'input_bills_detail': input_bill_detail,
        'sum': sum_price,
        'status': status
    }
    # truyền vào các giá trị khác như bình thường, lưu ý phải có lưu dữ liệu ở phía trước
    return render(request, 'Input_bill/input_bill_detail.html', context)


# OUTPUT
class OutputBillListView(PermissionRequiredMixin, ListView):
    permission_required = 'Bill.view_outputbill'
    model = OutputBill
    template_name = 'Output_Bill/list_output_bill.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'output_bills'
    ordering = ['-output_date']
    paginate_by = 10  # Số lượng phân trang

    def handle_no_permission(self):
        return redirect('Webshop:home')


class OutputBillUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView, ABC):
    model = OutputBill
    fields = ['customer', 'output_date', 'flag']
    template_name = 'Output_Bill/output_bill_form.html'
    success_url = 'output'

    def form_valid(self, form):
        form.instance.staff = self.request.user
        return super().form_valid(form)

    def test_func(self):
        input_bill = self.get_object()
        if self.request.user == input_bill.staff:
            return True
        return False


class OutputBillDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView, ABC):
    model = OutputBill
    success_url = 'output'
    template_name = 'Output_Bill/output_bill_confirm_delete.html'

    def test_func(self):
        output_bill = self.get_object()
        if self.request.user == output_bill.staff:
            return True
        return False

        
class OutputBillCreateView(LoginRequiredMixin, CreateView):
    model = OutputBill
    fields = ['customer', 'output_date', 'flag']  # field must contains in models
    template_name = 'Output_Bill/output_bill_form.html'

    def form_valid(self, form):
        form.instance.staff = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return self.object.get_absolute_url()

        
class DetailOutputUpdateView(LoginRequiredMixin, UpdateView, ABC):
    model = DetailOutputBill
    fields = ['warehouse', 'count']
    template_name = 'Output_Bill/detail_output_bill/detail_bill_update.html'
    old_data = []

    def get_context_data(self, **kwargs):
        pk = self.kwargs.get(self.pk_url_kwarg)  # use to get pk of objects
        context = super().get_context_data(**kwargs)
        context['warehouse'] = self.object.warehouse.product.name  # get data in the form when log in
        context['count'] = self.object.count
        self.old_data.clear()  # keep old data
        self.old_data.append(context['warehouse'])
        self.old_data.append(context['count'])
        return context

    def get_success_url(self):
        print(self.old_data)
        if self.old_data[0] == self.object.warehouse.product.name:
            warehouse = Warehouse.objects.get(product__name=self.object.warehouse.product.name)
            warehouse.count += self.old_data[1]
            warehouse.count -= self.object.count
            warehouse.save()
        else:
            warehouse = Warehouse.objects.get(product__name=self.old_data[0])
            warehouse.count += self.old_data[1]
            warehouse.save()
            warehouse_new = Warehouse.objects.get(product__name=self.object.warehouse.product.name)
            warehouse_new.count -= self.object.count
            warehouse_new.save()
        return self.object.get_update_return()


class DetailOutputDeleteView(LoginRequiredMixin, DeleteView, ABC):
    model = DetailOutputBill
    template_name = 'Output_Bill/detail_output_bill/detail_bill_delete.html'

    def get_success_url(self):
        return self.object.get_update_return()


class UserOutputBillListView(ListView):
    model = OutputBill
    template_name = 'Output_Bill/staff_output_bill.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'output_bills'  # using in template
    ordering = ['-output_date']
    paginate_by = 5  # Số lượng phân trang

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return OutputBill.objects.filter(staff=user).order_by('-output_date')


@login_required(login_url='login')
def create_detail_outputbill(request, pk):
    detail_output_bill_formset = inlineformset_factory(OutputBill, DetailOutputBill,
                                                       fields=('warehouse', 'count'), extra=10)
    # why use input_bill and detail_input because it has been created before now we need to
    # insert more than product in the input bill so we choice inlineformset like that
    output_bill = OutputBill.objects.get(id=pk)
    formset = detail_output_bill_formset(queryset=DetailOutputBill.objects.none(), instance=output_bill)
    if request.method == 'POST':
        formset = detail_output_bill_formset(request.POST, instance=output_bill)
        if formset.is_valid():
            for f in formset:
                # it run all for even not data in that so you have to make try catch to
                # remove the data not has enough data you need
                cd = f.cleaned_data
                warehouse_name = cd.get('warehouse')
                count = cd.get('count')
                # update data in warehouse
                try:
                    warehouse = Warehouse.objects.get(product__name=warehouse_name)
                except Warehouse.DoesNotExist:
                    warehouse = None
                if warehouse is not None:
                    warehouse.count -= count
                    warehouse.save()
                    print(warehouse.count)

            formset.save()
            return redirect('/list/output_bill')

    context = {'form': formset}
    return render(request, 'Output_Bill/detail_output_bill/output_bill_detail_form.html', context)


def all_detail_output_bill(request, pk):
    sum_price = 0
    status = "UnDeal"
    output_bill = OutputBill.objects.get(id=pk)
    if output_bill.flag == 1:
        status = "Deal"
    output_bill_detail = DetailOutputBill.objects.filter(output_bill__id=pk)
    for bill in output_bill_detail:
        bill.price = bill.warehouse.product.selling_price * bill.count
        sum_price += bill.price
    context = {
        'output_bill': output_bill,
        'output_bills_detail': output_bill_detail,
        'sum': sum_price,
        'status': status
    }
    # truyền vào các giá trị khác như bình thường, lưu ý phải có lưu dữ liệu ở phía trước
    return render(request, 'Output_Bill/output_bill_detail.html', context)