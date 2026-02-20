from django.urls import path
from . import views

urlpatterns = [
# Dashboard and Product
    path('',views.home,name='home'),
    path('product/',views.Prod,name='product'),
    path('customer/',views.customer,name='customer'),
    path('customer/<str:pk_test>/',views.customer,name='customer_detail'),
#order operations
    path('create_order/',views.createOrder,name='create_order'),    
    path('update_order/<str:pk>/',views.updateorder,name='update_order'),
    path('delete_order/<str:pk>/',views.deleteorder,name='delete_order'),
#customer operations
    path('create_customer/', views.create_customer, name='create_customer'),
    path('customer_list/', views.Customer_list, name='customer_list'),
    path('update_customer/<str:pk>/', views.update_customer, name='update_customer'),
    path('delete_customer/<str:pk>/', views.deletecustomer, name='delete_customer'),
    path('place_order/<str:pk>/', views.place_order, name='place_order'),
    
#product operations
    path('add_product/',views.add_product,name='add_product'),
    #didnt use delete products

#tag operations
    path('tag/',views.tag,name='tag'),
]
