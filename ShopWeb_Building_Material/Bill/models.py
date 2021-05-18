from django.db import models
from django.contrib.auth.models import User
from Provider.models import Provider
from Product.models import Product
from Customer.models import Customer
from Warehouse.models import Warehouse
from datetime import datetime    
from django.utils.translation import gettext as _ # using in datetime
from django.urls import reverse

# Create your models here.
class Bill(models.Model) :
    STATUS = (
        (1, 'Pending'),
        (0, 'Out for delivery'),
        (-1, 'Delivered'),
    )
    id = models.AutoField(primary_key=True)
    staff = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    flag = models.IntegerField(default=1, choices=STATUS)

    class Meta:
        abstract = True


class InputBill(Bill):
    provider = models.ForeignKey(Provider, on_delete=models.CASCADE, related_name="input_bills")
    input_date = models.DateField(_("Date"), default=datetime.today)

    def __str__(self):
        return str(self.provider)

    def get_absolute_url(self):
        return reverse('input-bill-detail-create', kwargs={'pk': self.pk})


class DetailInputBill(models.Model):
    id = models.AutoField(primary_key=True)
    product = models.ForeignKey(Product, null=True, on_delete=models.SET_NULL)
    input_bill = models.ForeignKey(InputBill, null=True, on_delete=models.SET_NULL)
    count = models.IntegerField(default=1)
    price = models.IntegerField(default=10000)

    def __str__(self):
        return str(self.product.name)

    def get_absolute_url(self):
        return reverse('input-bill-detail-create', kwargs={'pk': self.pk})

    def get_update_return(self):
        return reverse('input-bill-detail', kwargs={'pk': self.input_bill.pk})


# output
class OutputBill(Bill):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="output_bills")
    output_date = models.DateField(_("Date"), default=datetime.today)

    def __str__(self):
        return str(self.customer)

    def get_absolute_url(self):
        return reverse('output-bill-detail-create', kwargs={'pk': self.pk})


class DetailOutputBill(models.Model):
    id = models.AutoField(primary_key=True)
    warehouse = models.ForeignKey(Warehouse, null=True, on_delete=models.SET_NULL)
    output_bill = models.ForeignKey(OutputBill, null=True, on_delete=models.SET_NULL)
    count = models.IntegerField(default=1)
    price = models.IntegerField(default=10000)

    def __str__(self):
        return str(self.warehouse.product.name)

    def get_absolute_url(self):
        return reverse('output-bill-detail-create', kwargs={'pk': self.pk})

    def get_update_return(self):
        return reverse('output-bill-detail', kwargs={'pk': self.output_bill.pk})