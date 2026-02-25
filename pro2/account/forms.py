from django.forms import ModelForm
from .models import Order,Customer, Product

class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = '__all__'

class CustomerForm(ModelForm):
    class Meta:
        model = Customer
        fields = '__all__'
        
class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = '__all__'

# User registration form
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']