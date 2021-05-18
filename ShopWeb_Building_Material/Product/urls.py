from django.urls import path
from Product import views
from .views import *

app_name ='Product'
urlpatterns = [
    path('', ProductListView.as_view(), name='list-product'),    
    path('new/', ProductCreateView.as_view(), name="product-create"),
    path('<int:pk>/update/', ProductUpdateView.as_view(), name='product-update'),
    path('<int:pk>/delete/', ProductDeleteView.as_view(), name='product-delete'),
    path('<int:pk>', ProductDetailView.as_view(), name='product-detail'),
    path('<str:type_product>', views.List_typeProduct, name='product-list-type'),

]