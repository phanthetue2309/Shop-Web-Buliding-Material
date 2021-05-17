from django.db import models
from Product.models import Product

# Create your models here.
class Warehouse(models.Model):
    id = models.AutoField(primary_key=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="warehouses", blank=True,
                                null=True)
    count = models.IntegerField(default=0, blank=True, null=True)

    def __str__(self):
        return str(self.product.name)

    class Meta:
        ordering = ['product__type_product__name']