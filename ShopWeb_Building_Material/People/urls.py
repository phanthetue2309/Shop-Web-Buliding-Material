from django.urls import path
from .views import *

app_name = 'People'
urlpatterns = [
    path('customer/', CustomerListView.as_view(), name='list-customer'),
    path('provider/', ProviderListView.as_view(), name='list-provider'),
    
]