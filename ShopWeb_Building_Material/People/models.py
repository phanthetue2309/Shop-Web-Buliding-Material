from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

class AbstractPerson(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=45)
    address = models.CharField(max_length=45, null=True)
    phone_number = models.CharField(max_length=45, null=True)
    discription = models.TextField(null=True)
    
    def __str__(self):  # show the name of customer when print
        return self.name

    class Meta:
        abstract = True


class Customer(AbstractPerson):
    pass

    def get_absolute_url(self):
            return reverse('People:list-customer')
    

class Provider(AbstractPerson):
    website = models.CharField(max_length=45, null=True)
    email = models.CharField(max_length=45, null=True)
    
    def get_absolute_url(self):
            return reverse('People:list-provider')