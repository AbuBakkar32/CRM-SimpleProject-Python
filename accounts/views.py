from datetime import datetime

from django.shortcuts import render, redirect
from django.forms import inlineformset_factory
from .filters import OrderFilter
from .models import *
from .forms import OrderForm, CustomerForm


def home(request):
    orders = Order.objects.all()
    customers = Customer.objects.all()
    total_customers = customers.count()
    total_orders = orders.count()
    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count()
    date = datetime.now()

    context = {'total_customers': total_customers, 'orders': orders, 'customers': customers,
               'total_orders': total_orders, 'delivered': delivered,
               'pending': pending, 'date': date}

    return render(request, 'accounts/dashboard.html', context)


def products(request):
    products = Product.objects.all()
    date = datetime.now()
    return render(request, 'accounts/products.html', {'products': products, 'date': date})


def updateCustomer(request, pk):
    cus = Customer.objects.get(id=pk)
    form = CustomerForm(instance=cus)
    if request.method == 'POST':
        form = CustomerForm(request.POST, instance=cus)
        if form.is_valid():
            form.save()
            return redirect('/')
    context = {'form': form}
    return render(request, 'accounts/customer_form.html', context)


def customer(request, pk_test):
    customer = Customer.objects.get(id=pk_test)
    orders = customer.order_set.all()
    order_count = orders.count()
    myFilter = OrderFilter(request.GET, queryset=orders)
    orders = myFilter.qs
    date = datetime.now()
    context = {'customer': customer, 'orders': orders, 'order_count': order_count,
               'myFilter': myFilter, 'date': date}
    return render(request, 'accounts/customer.html', context)


def createOrder(request, pk):
    OrderFormSet = inlineformset_factory(Customer, Order, fields=('product', 'status'), extra=10)
    customer = Customer.objects.get(id=pk)
    formset = OrderFormSet(queryset=Order.objects.none(), instance=customer)
    # form = OrderForm(initial={'customer':customer})
    if request.method == 'POST':
        formset = OrderFormSet(request.POST, instance=customer)
        if formset.is_valid():
            formset.save()
            return redirect('/')
    context = {'form': formset}
    return render(request, 'accounts/order_form.html', context)


def updateOrder(request, pk):
    order = Order.objects.get(id=pk)
    form = OrderForm(instance=order)
    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('/')
    context = {'form': form}
    return render(request, 'accounts/order_form.html', context)


def deleteOrder(request, pk):
    order = Order.objects.get(id=pk)
    if request.method == "POST":
        order.delete()
        return redirect('/')
    context = {'item': order}
    return render(request, 'accounts/delete.html', context)
