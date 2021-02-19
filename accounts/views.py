from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import *
from .forms import *
from .filters import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import Group
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .decorators import unauthenticated_user,allowed_users,admin_only


@unauthenticated_user
def registerPage(request):
	form = CreationUserForm()
	if request.method == 'POST':
		form = CreationUserForm(request.POST)
		if form.is_valid():
			user = form.save()

			username=form.cleaned_data.get('username')


			messages.success(request,'Account was created for'+username)
			return redirect('login')

	context = {'form':form}
	return render(request,'accounts/register.html',context)

@unauthenticated_user
def loginPage(request):
	if request.method=='POST':
		username = request.POST.get('username')
		password = request.POST.get('password')

		user = authenticate(request, username= username, password=password)

		if user is not None:
			login(request,user)
			return redirect('/home')
		else:
			messages.info(request,"username And Password Incorrect")	

	context={}		
	return render(request,'accounts/login.html',context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def userpage(request):
	orders = request.user.customer.order_set.all()

	total_order = orders.count()
	delivered = orders.filter(status='Delivered').count()
	pending = orders.filter(status='Panding').count()


	#print('ORDERS':orders)

	context  = {'orders':orders,
				'total_order':total_order,
				'delivered':delivered,
				'pending':pending
				}
	return render(request,'accounts/user.html', context)



@allowed_users(allowed_roles=['customer'])
@login_required(login_url='login')
def accountSetting(request):
	customer = request.user.customer
	form = CustomerForm(instance=customer)
	

	if request.method =='POST':
		form = CustomerForm(request.POST, request.FILES, instance=customer)
		if form.is_valid():
			form.save()

	context ={'form':form}
	return render(request,'accounts/account_setting.html',context)		




def logoutUser(request):
	logout(request)
	return redirect('login')


@login_required(login_url='login')
@admin_only
def home(request):
	orders = Order.objects.all()
	customers = Customer.objects.all()

	total_customer =orders.count()

	total_order = orders.count()
	delivered = orders.filter(status='Delivered').count()
	pending = orders.filter(status='Panding').count()

	context = { 'orders':orders, 
				'customers':customers,
				'total_order':total_order,
				'total_customer':total_customer,
				'delivered':delivered,
				'pending':pending
			   }

	return render(request,'accounts/dashboard.html',context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def product(request):

	products = Product.objects.all()

	return render(request,'accounts/product.html',{'products':products})


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def customer(request,pk):
	customer = Customer.objects.get(id=pk)

	orders = customer.order_set.all()

	order_count = orders.count()

	myFilter = OrderFilter(request.GET, queryset=orders)

	orders= myFilter.qs

	context={'customer':customer, 'orders':orders, 'order_count':order_count,
	'myFilter':myFilter}

	return render(request,'accounts/customer.html',context)	



@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def create_order(request,pk):
	customer = Customer.objects.get(id=pk)  
	if request.method == 'POST':
		form = createOrder(request.POST)
		if form.is_valid():
			form.save()
			return redirect('/')
	else:
		form=createOrder(initial={'customer':customer}) 	
		context={'form':form}
		return render(request,'accounts/create_order.html',context)	



@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def update_order(request,pk):
	order = Order.objects.get(id=pk)
	form = createOrder(instance=order)
	if request.method == 'POST':
		form = createOrder(request.POST, instance=order)
		if form.is_valid():
			form.save()
			return redirect('/')


	context= {'form':form}
	return render(request,'accounts/create_order.html',context)



@login_required(login_url='login')	  
@allowed_users(allowed_roles=['admin'])
def delete_order(request,pk):
	delete_order=Order.objects.get(id=pk)
	if request.method=='POST':
		delete_order.delete()
		return redirect('/')

	context={'item':delete_order}
	return render(request,'delete_order.html',context)


