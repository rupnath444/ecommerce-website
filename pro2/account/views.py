from django.shortcuts import render,redirect
from .models import Customer, Order, Product, Tag
from .forms import OrderForm,CustomerForm
# Create your views here.

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

def Prod(request):
    product = Product.objects.all()
    context = {'product': product}
    return render(request, 'account/product.html', context)


def createOrder(request):
    form = OrderForm()
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
    context = {'form': form}
    return render(request, 'account/order_form.html', context)

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

def createcustomer(request):
    form = CustomerForm()
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    context = {'form': form}
    return render(request, 'account/create_customer.html', context)

def Customer_list(request):
    customers = Customer.objects.all()
    context = {'customers': customers}
    return render(request, 'account/customer_list.html', context)


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

    
def tag(request):
    tags = Tag.objects.all()
    context = {'tags': tags}
    return render(request, 'account/tag.html', context)