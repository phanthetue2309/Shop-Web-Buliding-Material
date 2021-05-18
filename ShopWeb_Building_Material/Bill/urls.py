from django.urls import path
from Bill import views
from .views import *

app_name = 'Bill'
urlpatterns = [
    # input 
    path('input/', InputBillListView.as_view(), name='list-input'),
    path('staff/input/<str:username>', UserInputBillListView.as_view(), name='staff-input-bill'),
    path('input/<int:pk>', views.all_detail_input_bill, name='input-bill-detail'),
    path('input/<int:pk>/update/', InputBillUpdateView.as_view(), name='input-bill-update'),
    path('input/<int:pk>/delete/', InputBillDeleteView.as_view(), name='input-bill-delete'),
    path('input/new/', InputBillCreateView.as_view(), name='input-bill-create'),
    
    path('detail_input_bill/<int:pk>/', views.create_detail_inputbill, name='input-bill-detail-create'),
    path('update_detail_input_bill/<int:pk>/', DetailInputUpdateView.as_view(), name='update-detail-input-bill'),
    path('delete_detail_input_bill/<int:pk>/', DetailInputDeleteView.as_view(), name='delete-detail-input-bill'),


    # output
    path('output/', OutputBillListView.as_view(), name='list-output'),    
    path('output/new/', OutputBillCreateView.as_view(), name='output-bill-create'),
    path('output/<int:pk>', views.all_detail_output_bill, name='output-bill-detail'),
    path('output/<int:pk>/update/', OutputBillUpdateView.as_view(), name='output-bill-update'),
    path('output/<int:pk>/delete/', OutputBillDeleteView.as_view(), name='output-bill-delete'),
    path('staff/output/<str:username>', UserOutputBillListView.as_view(), name='staff-output-bill'),
    # show the detail output bill
    path('detail_output_bill/<int:pk>/', views.create_detail_outputbill, name='output-bill-detail-create'),
    path('update_detail_output_bill/<int:pk>/', DetailOutputUpdateView.as_view(), name='update-detail-output-bill'),
    path('delete_detail_output_bill/<int:pk>/', DetailOutputDeleteView.as_view(), name='delete-detail-output-bill'),


]