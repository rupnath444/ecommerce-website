from django.urls import path
from . import views

urlpatterns = [
    path('',views.home,name='home'),
    path('product/',views.Prod,name='product'),
    path('customer/',views.customer,name='customer'),
    path('customer/<str:pk_test>/',views.customer,name='customer_detail'),
    path('create_order/',views.createOrder,name='create_order'),    
    path('update_order/<str:pk>/',views.updateorder,name='update_order'),
    path('delete_order/<str:pk>/',views.deleteorder,name='delete_order'),
#customer operations
    path('create_customer/',views.createcustomer,name='create_customer'),
    path('tag/',views.tag,name='tag'),
]