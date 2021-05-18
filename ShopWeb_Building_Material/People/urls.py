from django.urls import path
from .views import *

app_name = 'People'
urlpatterns = [
    # Url Customer
    path('customer/', CustomerListView.as_view(), name='list-customer'),
    path('customer/new', CustomerCreateView.as_view(), name="customer-create"),
    path('customer/<int:pk>/update/', CustomerUpdateView.as_view(), name='customer-update'),
    path('customer/<int:pk>/delete/', CustomerDeleteView.as_view(), name='customer-delete'),
    path('customer/<int:pk>', CustomerDetailView.as_view(), name='customer-detail'),
    # Url Provider
    path('provider/', ProviderListView.as_view(), name='list-provider'),
    path('provider/new', ProviderCreateView.as_view(), name="provider-create"),
    path('provider/<int:pk>/update/', ProviderUpdateView.as_view(), name='provider-update'),
    path('provider/<int:pk>/delete/', ProviderDeleteView.as_view(), name='provider-delete'),
    path('provider/<int:pk>', ProviderDetailView.as_view(), name='provider-detail'),
    
]