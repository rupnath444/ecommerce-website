from multiprocessing import context

from django.shortcuts import render, redirect
from .models import Customer, Order, Product, Tag
from .forms import OrderForm, CustomerForm, ProductForm
from django.forms import inlineformset_factory
from .filters import OrderFilter
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import csv
from .forms import CreateUserForm
# Create your views here.
#dashboard Operations



def registration(request):
    if request.user.is_authenticated:
        return redirect('home')
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    context = {'form': form}
    return render(request, 'account/registration.html', context)

def loginpage(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.info(request, 'Username OR password is incorrect')
        context = {}
        return render(request, 'account/login.html', context)

def logoutUser(request):
    from django.contrib.auth import logout
    logout(request)
    return redirect('login')

@login_required(login_url='login')
def home(request):
    orders = Order.objects.all()
    customers = Customer.objects.all()
    total_orders = orders.count()
    orders_delivered = orders.filter(status='Delivered').count()
    orders_pending = orders.filter(status='Pending').count()
    out_for_delivery = orders.filter(status='Out for delivery').count() 
    context = {
        'total_orders': total_orders,
        'orders_delivered': orders_delivered,
        'orders_pending': orders_pending,
        'out_for_delivery': out_for_delivery,
        'customers': customers,
        'orders': orders
    }
    return render(request, 'account/dashboard.html', context)

@login_required(login_url='login')
def createOrder(request):
    form = OrderForm()
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
    context = {'form': form}
    return render(request, 'account/order_form.html', context)


@login_required(login_url='login')
def create_customer(request):
    form = CustomerForm()
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    context = {'form': form}
    return render(request, 'account/create_customer.html', context)



@login_required(login_url='login')
def Order_list(request):
    status = request.GET.get('status')
    if status:
        orders = Order.objects.filter(status=status)
    else:
        orders = Order.objects.all()
    context = {'orders': orders}
    return render(request, 'account/order_list.html', context)

###############################################################################################

@login_required(login_url='login')
def Prod(request):
    product = Product.objects.all()
    context = {'product': product}
    return render(request, 'account/product.html', context)

@login_required(login_url='login')
def customer(request, pk_test=None):
    if pk_test:
        try:
            customer = Customer.objects.get(id=pk_test)
        except Customer.DoesNotExist:
            customer = None
        orders = customer.order_set.all() if customer else []
        order_count = orders.count() if customer else 0
        myfilter = OrderFilter(request.GET, queryset=orders)
        orders = myfilter.qs
        context = {'customer': customer, 'orders': orders, 'order_count': order_count, 'myfilter': myfilter}
    else:
        customers = Customer.objects.all()
        context = {'customers': customers}
    return render(request, 'account/customer.html', context)



@login_required(login_url='login')
def updateorder(request, pk):
    order = Order.objects.get(id=pk)
    form = OrderForm(instance=order)
    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('/')
    context = {'form': form}
    return render(request, 'account/order_form.html', context)


@login_required(login_url='login')
def deleteorder(request, pk):
    order = Order.objects.get(id=pk)
    if request.method == 'POST':
        order.delete()
        return redirect('/')
    context = {'item': order}
    return render(request, 'account/delete.html', context)


@login_required(login_url='login')
def place_order(request, pk):
    customer = Customer.objects.get(id=pk)
    orderformset = inlineformset_factory(Customer, Order, fields=('product', 'status'), extra=7)
    formset = orderformset(queryset=Order.objects.none(), instance=customer)
    if request.method == 'POST':
        formset = orderformset(request.POST, instance=customer)
        if formset.is_valid():
            formset.save()
            return redirect('home')
    context = {'form': formset, 'customer': customer}
    return render(request, 'account/place_order.html', context)


@login_required(login_url='login')
def Customer_list(request):
    customers = Customer.objects.all()
    context = {'customers': customers}
    return render(request, 'account/customer_list.html', context)



@login_required(login_url='login')
def update_customer(request, pk):
    customer = Customer.objects.get(id=pk)
    form = CustomerForm(instance=customer)
    if request.method == 'POST':
        form = CustomerForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            return redirect('customer_detail', pk_test=pk)
    context = {'form': form, 'customer': customer}
    return render(request, 'account/create_customer.html', context)


@login_required(login_url='login')
def deletecustomer(request, pk):
    customer = Customer.objects.get(id=pk)
    if request.method == 'POST':
        customer.delete()
        return redirect('customer_list')
    context = {'item': customer}
    return render(request, 'account/delete.html', context)


@login_required(login_url='login')
def add_product(request):
    form = ProductForm()
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('product')
    context = {'form': form}
    return render(request, 'account/add_product.html', context)


@login_required(login_url='login')
def update_product(request, pk):
    product = Product.objects.get(id=pk)
    form = ProductForm(instance=product)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('product')
    context = {'form': form, 'product': product}
    return render(request, 'account/add_product.html', context)

@login_required(login_url='login')
def deleteproduct(request, pk):
    product = Product.objects.get(id=pk)
    if request.method == 'POST':
        product.delete()
        return redirect('product')
    context = {'item': product}
    return render(request, 'account/delete.html', context)


@login_required(login_url='login')
def tag_list(request):
    tags = Tag.objects.all()
    context = {'tags': tags}
    return render(request, 'account/tag.html', context)


@login_required(login_url='login')
def importtag(request):
    if request.method == "POST":
        csv_file = request.FILES.get("file")
        decoded_file = csv_file.read().decode('utf-8').splitlines()
        reader = csv.DictReader(decoded_file)
        for row in reader:
            Tag.objects.get_or_create(name=row['name'])
        return redirect('tag')
    return render(request, 'account/managing_tag.html')

