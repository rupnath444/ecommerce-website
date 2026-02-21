from django.shortcuts import render, redirect
from .models import Customer, Order, Product, Tag
from .forms import OrderForm, CustomerForm, ProductForm
from django.forms import inlineformset_factory
import csv

# Create your views here.
#dashboard Operations
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

def createOrder(request):
    form = OrderForm()
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
    context = {'form': form}
    return render(request, 'account/order_form.html', context)

def create_customer(request):
    form = CustomerForm()
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    context = {'form': form}
    return render(request, 'account/create_customer.html', context)


def Order_list(request):
    status = request.GET.get('status')
    if status:
        orders = Order.objects.filter(status=status)
    else:
        orders = Order.objects.all()
    context = {'orders': orders}
    return render(request, 'account/order_list.html', context)

###############################################################################################
def Prod(request):
    product = Product.objects.all()
    context = {'product': product}
    return render(request, 'account/product.html', context)


def customer(request, pk_test=None):
    if pk_test:
        try:
            customer = Customer.objects.get(id=pk_test)
        except Customer.DoesNotExist:
            customer = None
        orders = customer.order_set.all() if customer else []
        order_count = orders.count() if customer else 0
        context = {'customer': customer, 'orders': orders, 'order_count': order_count}
    else:
        customers = Customer.objects.all()
        context = {'customers': customers}
    return render(request, 'account/customer.html', context)


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

def deleteorder(request, pk):
    order = Order.objects.get(id=pk)
    if request.method == 'POST':
        order.delete()
        return redirect('/')
    context = {'item': order}
    return render(request, 'account/delete.html', context)

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


def Customer_list(request):
    customers = Customer.objects.all()
    context = {'customers': customers}
    return render(request, 'account/customer_list.html', context)


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

def deletecustomer(request, pk):
    customer = Customer.objects.get(id=pk)
    if request.method == 'POST':
        customer.delete()
        return redirect('customer_list')
    context = {'item': customer}
    return render(request, 'account/delete.html', context)

def add_product(request):
    form = ProductForm()
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('product')
    context = {'form': form}
    return render(request, 'account/add_product.html', context)

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

def deleteproduct(request, pk):
    product = Product.objects.get(id=pk)
    if request.method == 'POST':
        product.delete()
        return redirect('product')
    context = {'item': product}
    return render(request, 'account/delete.html', context)

def tag_list(request):
    tags = Tag.objects.all()
    context = {'tags': tags}
    return render(request, 'account/tag.html', context)

def importtag(request):
    if request.method == "POST":
        csv_file = request.FILES.get("file")
        decoded_file = csv_file.read().decode('utf-8').splitlines()
        reader = csv.DictReader(decoded_file)
        for row in reader:
            Tag.objects.get_or_create(name=row['name'])
        return redirect('tag')
    return render(request, 'account/managing_tag.html')