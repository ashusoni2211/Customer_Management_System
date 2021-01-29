from django.shortcuts import render,redirect

from .forms import OrderForm,RegisterForm,CustomerForm
from django.forms import inlineformset_factory
from .filters import orderFilter

from django.contrib import messages 
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from .decoraters import unauthenticated_user,allowed_user,admin_only
from django.contrib.auth.models import Group

from .models import *

# Create your views here.

@unauthenticated_user
def registerPage(request):
    form = RegisterForm()
    if request.method=='POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            
           
            
            messages.success(request , 'Account was created ')
            return redirect('loginPage')
    content = {
        'form':form
    }
    return render(request,'register.html',content)

@unauthenticated_user
def loginPage(request):
    if request.method == 'POST':
        username=request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            messages.info(request,'username or password is incorrect')
            return render(request,'login.html')

    return render(request,'login.html')

def logoutUser(request):
    logout(request)
    return redirect('loginPage')

@login_required(login_url='loginPage')
@admin_only
def home(request):
    customer = Customer.objects.all()
    order = Order.objects.all()
    totalOrder = order.count()
    delivered = order.filter(status='Delivered').count()
    pending = totalOrder-delivered
    content = {
        'customer':customer,
        'order':order,
        'totalOrder':totalOrder,
        'delivered':delivered,
        'pending':pending

    }
    return render(request,'dashboard.html',content)

@login_required(login_url='loginPage')
def userPage(request):
    order = request.user.customer.order_set.all()
    totalOrder = order.count()
    delivered = order.filter(status='Delivered').count()
    pending = totalOrder-delivered
    content = {
        'order':order,
        'totalOrder':totalOrder,
        'delivered':delivered,
        'pending':pending
    }
    return render(request,'user.html',content)

@login_required(login_url='loginPage')
@allowed_user(allowed_roles=['customer'])
def accountSetting(request):
    customer = request.user.customer
    form  = CustomerForm(instance=customer)
    if request.method == 'POST':
        form = CustomerForm(request.POST, request.FILES, instance=customer)
        if form.is_valid():
            form.save()
    content = {
        'form':form
    }
    return render(request , 'account_setting.html',content)


@login_required(login_url='loginPage')
@allowed_user(allowed_roles=['admin'])
def product(request):
    product = Product.objects.all()
    content = {
        'product':product
    }
    return render(request,'products.html',content)

@login_required(login_url='loginPage')
@allowed_user(allowed_roles=['admin'])
def customer(request,pk):
    customer = Customer.objects.get(id=pk)
    order = customer.order_set.all()
    totalOrder = order.count()
    filterSet = orderFilter(request.GET,queryset=order)
    order = filterSet.qs
    content = {
        'customer':customer,
        'order':order,
        'totalOrder':totalOrder,
        'filterSet':filterSet
    }
    return render(request,'customer.html',content)

@login_required(login_url='loginPage')
@allowed_user(allowed_roles=['admin'])
def createOrder(request,pk):
    orderFormSet = inlineformset_factory(Customer,Order,fields = ('product','status'),extra=10)
    customer = Customer.objects.get(id=pk)
    formset = orderFormSet(queryset=Order.objects.none(),instance=customer)
    if request.method=='POST':
        formset = orderFormSet(request.POST,instance=customer)
        if formset.is_valid():
            formset.save()
            return redirect('home')
    content = {
        'formset':formset
    }
    return render(request,'order_form.html',content)

@login_required(login_url='loginPage')
@allowed_user(allowed_roles=['admin'])
def updateOrder(request,pk):
    order = Order.objects.get(id=pk)
    form = OrderForm(instance=order)
    if request.method == 'POST':
        form  = OrderForm(request.POST,instance=order)
        if form.is_valid():
            form.save()
            return redirect('home')
    content = {
        'form':form
    }
    return render(request,'update_order.html',content)


@login_required(login_url='loginPage')
@allowed_user(allowed_roles=['admin'])
def delete(request,pk):
    order = Order.objects.get(id=pk)
    if request.method == 'POST':
        order.delete()
        return redirect('home')
    content = {
        'order':order
    }
    return render(request,'delete.html',content)
