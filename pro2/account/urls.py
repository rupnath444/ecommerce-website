from django.urls import path
from . import views

urlpatterns = [
# Dashboard area
    path('',views.home,name='home'),
    path('order_list/',views.Order_list,name='order_list'),
    
#navbar operations
    path('product/',views.Prod,name='product'),
    path('customer/<str:pk_test>/',views.customer,name='customer_detail'),
    path('tag/',views.tag_list,name='tag'),
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
    path('delete_product/<str:pk>/',views.deleteproduct,name='delete_product'),
    path('update_product/<str:pk>/',views.update_product,name='update_product'),
    

#tag operations
    
    path('import_tag/',views.importtag,name='import_tag'),
]
