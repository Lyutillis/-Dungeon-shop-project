from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import User
from product.models import Product, Category
from product.utils import cartData, cookieCart, sessionPath, guestOrder
from django.http import HttpRequest
import json
import os

# Create your views here.
def homepage_view(request) :
	path = sessionPath(request, '/')
	context={'product_list':None, 'items': None, 'order': None, 'cartItems': None}
	product_list=Product.objects.all()
	context['product_list']=product_list
	data = cartData(request)
	context['items'] = data['items']
	context['order'] = data['order']
	context['cartItems'] = data['cartItems']
	context['categories'] = list(Category.objects.all())
	return render(request, 'homepage.html', context)

def login_view(request):
	path = sessionPath(request, '/login/')
	context = {'login_data_error': False,
               'invalid_data_error': False,
               'email': None,
    }
	data = cartData(request)
	context['cartItems'] = data['cartItems']
	if request.method == 'POST' :
		email = request.POST.get('email')
		password = request.POST.get('password')
		if not len(email) or not len(password) :
			context['login_data_error']=True
			context['email'] = email
			messages.success(request, ("Не все поля заполнены (логин)!"))
			return render(request, 'login.html', context)
		user = authenticate(request, email = email, password = password)
		if user : 
			user.update(is_active=True)
			login(request, user)
			guestOrder(request, email)
			messages.success(request, ("Должно было прокатить (логин)!"))
			return redirect(path)
		else:
			context['invalid_data_error'] = True
			context['email'] = email
			messages.success(request, ("походу не прокатило (логин)!"))
			return render(request, 'login.html', context=context)
	return render(request, 'login.html', context=context)

def register_view(request):
	path = sessionPath(request, '/register/')
	context = {'register_data_error': False,
               'password_equity_error': False,
               'email_error': False,
               'created': False,
               'email': None,
    }
	if request.method== 'POST' :
		email = request.POST.get('email')
		password1 = request.POST.get('password1')
		password2 = request.POST.get('password2')
		username=request.POST.get('username')
		if not len(email) or not len(password1) or not len(password2):
			context['email']=email
			context['register_data_error']=True
			messages.success(request, ("Не все поля заполнены (регистр)!"))
			return render(request, 'register.html', context)
		if password1 != password2 :
			context['password_equity_error']=True
			context['email']=email
			messages.success(request, ("Пароли не совпадают (регистр)!"))
			return render(request, 'register.html', context)
		user=User.objects.create_user(email, password1)
		if user :
			user = authenticate(request, email = email, password = password1) 
			context['created'] = True
			user.update(is_active=True, username=username)
			login(request, user)
			messages.success(request, ("Зарегано (регистр) и войдено!"))
			return render(request, 'homepage.html', context=context)
		else :
			context['email_error'] = True
			context['email']=email
			messages.success(request, ("Почта уже зарегистрирована (регистр)!"))
			return render(request, 'register.html', context=context)
	return render(request, 'register.html', context=context)

def logout_view(request):
	logout(request)
	messages.success(request, ("You were Logged Out!")) 
	return redirect('/')

def profile_view(request):
	path = sessionPath(request, '/profile/')
	context={}
	data = cartData(request)
	context['cartItems'] = data['cartItems']
	if request.method == 'POST':
		user=request.user
		user.username=request.POST.get('username')
		user.email=request.POST.get('email')

		if request.FILES.get('image') :
			user.profile_pic = request.FILES.get('image')
			user.save()
		
		messages.success(request, ('Successfully altered!'))
	return render(request, 'profile.html', context)