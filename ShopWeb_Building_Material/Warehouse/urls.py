from django.urls import path
from .views import *

app_name = 'Warehouse'
urlpatterns = [
    path('', WarehouseListView.as_view(), name='warehouse'),    

]