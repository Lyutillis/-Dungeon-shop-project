from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import JsonResponse
from user.models import User
import datetime
import json
from .models import Product, Order, OrderItem, ShippingAddress, Comment, ReplyComment, Reply
import os
from .utils import cookieCart, cartData, guestOrder, sessionPath

def processOrder(request):
	transaction_id = datetime.datetime.now().timestamp()
	data = json.loads(request.body)


	customer = request.user
	order, created = Order.objects.get_or_create(customer=customer, complete=False)

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
	path = sessionPath(request, '/checkout/')
	data = cartData(request)
	cartItems = data['cartItems']
	order = data['order']
	items =  data['items']
	return render(request, 'checkout.html', {'items': items, 'order': order, 'cartItems': cartItems})

def cart_view(request):
	path = sessionPath(request, '/cart/')
	data = cartData(request)
	cartItems = data['cartItems']
	order = data['order']
	items =  data['items']
	return render(request, 'cart.html', {'items': items, 'order': order, 'cartItems': cartItems})

def product_page_view(request, id) :
	path = sessionPath(request, '/product-page/' + str(id))
	data = cartData(request)
	cartItems = data['cartItems']
	order = data['order']
	items =  data['items']
	product=Product.get_by_id(id)

	comments = Comment.objects.filter(product = product)[::-1]

	replies = {}

	for i in comments:
		try:
			reply = Reply.objects.filter(comment=i)
			replies[i] = list(reply)
		except:
			pass
	for i in replies:
		print(replies.get(i)) 


	return render(request, 'product_page.html', {'product': product, 'items': items, 'order': order, 'cartItems': cartItems, 'comments': comments, 'replies': replies})

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

def publishComment(request, id):
	path = sessionPath(request, '/product-page/'+str(id))
	if request.method == 'POST' :
		rating = request.POST.getlist('rating')
		content = request.POST.get('content')
		product = Product.objects.get(id=id)
		comment = Comment.objects.create(customer = request.user, product = product, body = content, rating = int(rating[0]))		
		comment.save()
		messages.success(request, ("Комментарий успешно добавлен!"))
		return redirect(path)
	messages.success(request, ("Комментарий не был добавлен!"))
	return redirect(path)

def publishReply(request, id):
	path = sessionPath(request, '/product-page/' + str(id))
	if request.method == 'POST' :
		content = request.POST.get('content')
		comment = Comment.objects.get(id=id)
		replycomment = ReplyComment.objects.create(customer = request.user, body = content)
		replycomment.save()
		reply = Reply.objects.create(comment=comment, reply=replycomment)
		messages.success(request, ("Reply успешно добавлен!"))
		return redirect(path)
	messages.success(request, ("Reply не был добавлен!"))
	return redirect(path)		
