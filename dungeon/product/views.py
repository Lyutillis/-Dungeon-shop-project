from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import JsonResponse
from user.models import User
import datetime
import json
from .models import Product, Order, OrderItem, ShippingAddress
import os
from .utils import cookieCart, cartData, guestOrder

def processOrder(request):
	transaction_id = datetime.datetime.now().timestamp()
	data = json.loads(request.body)

	if request.user.is_authenticated:
		customer = request.user
		order, created = Order.objects.get_or_create(customer=customer, complete=False)
	else:
		customer, order = guestOrder(request, data)

	total = float(data['form']['total'])
	order.transaction_id = transaction_id

	if total == order.get_cart_total:
		order.complete = True
		
	order.save()

	ShippingAddress.objects.create(
			customer = customer,
			order = order,
			address = data['shipping']['address'],
			city = data['shipping']['city'],
			zipcode = data['shipping']['zipcode'],
		)

	return JsonResponse('Payment submitted', safe=False)

def checkout(request):
	data = cartData(request)
	cartItems = data['cartItems']
	order = data['order']
	items =  data['items']
	return render(request, 'checkout.html', {'items': items, 'order': order, 'cartItems': cartItems})

def cart_view(request):
	data = cartData(request)
	cartItems = data['cartItems']
	order = data['order']
	items =  data['items']
	return render(request, 'cart.html', {'items': items, 'order': order, 'cartItems': cartItems})

def product_page_view(request, id) :
	data = cartData(request)
	cartItems = data['cartItems']
	order = data['order']
	items =  data['items']
	product=Product.get_by_id(id)
	return render(request, 'product_page.html', {'product': product, 'items': items, 'order': order, 'cartItems': cartItems})

def update_item(request):
	data = json.loads(request.body)
	productId=data['productId']
	action=data['action']

	print('action:', action)
	print('prodcut id:', productId)

	customer = request.user

	print(customer)

	product = Product.objects.get(id=productId)
	order, created = Order.objects.get_or_create(customer = customer, complete=False)

	orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

	if action == 'add' :
		orderItem.quantity = (orderItem.quantity + 1)
	elif action == 'remove' :
		orderItem.quantity = (orderItem.quantity - 1)

	orderItem.save()

	if orderItem.quantity <= 0 :
		orderItem.delete()

	return JsonResponse('Item was added', safe = False)