from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import JsonResponse
from user.models import User
import datetime
import json
from .models import Product, Order, OrderItem, ShippingAddress, Comment, ReplyComment, Reply, Category, SubCategory, PictureList, Rating
import os
from .utils import cookieCart, cartData, guestOrder, sessionPath
from django.db.models import Q
from django.forms.models import model_to_dict

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
	rating, created = Rating.objects.get_or_create(product=product)
	quantity = rating.quantity

	comments = Comment.objects.filter(product = product)[::-1]

	replies = {}

	for i in comments:
		try:
			reply = Reply.objects.filter(comment=i)
			replies[i] = list(reply)
		except:
			pass


	return render(request, 'product_page.html', {'product': product, 'items': items, 'order': order, 'cartItems': cartItems, 'comments': comments, 'replies': replies, 'rating': round(rating.overall), 'quantity': quantity,})

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
		rate = request.POST.getlist('rating')
		content = request.POST.get('content')
		product = Product.objects.get(id=id)
		comment = Comment.objects.create(customer = request.user, product = product, body = content, rating = int(rate[0]))		
		comment.save()
		rating, created = Rating.objects.get_or_create(product=product)
		rating.quantity += 1
		rating.stars += int(rate[0])
		rating.overall = rating.stars/rating.quantity
		rating.save()
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

def user_list_view(request):
	path = sessionPath(request, '/user-list/')
	data = cartData(request)
	cartItems = data['cartItems']
	users = User.objects.filter(~Q(id=request.user.id))
	
	return render(request, 'user_list.html', {'users': users, 'cartItems': cartItems})

def updatePermissionSuperuser(request):
	data = json.loads(request.body)
	userId=data['userId']
	action=data['action']

	print('action:', action)
	print('user id:', userId)

	user = User.objects.get(id = int(userId))

	print(user)

	if action == 'True' :
		user.is_superuser = True
	elif action == 'False' :
		user.is_superuser = False

	user.save()

	return JsonResponse('User permissions were updated!', safe = False)

def updatePermissionStaff(request):
	print('In views')
	data = json.loads(request.body)
	userId=data['userId']
	action=data['action']

	print('action:', action)
	print('user id:', userId)

	user = User.objects.get(id = int(userId))

	print(user)

	if action == 'True' :
		user.is_staff = True
	elif action == 'False' :
		user.is_staff = False

	user.save()

	return JsonResponse('User permissions were updated!', safe = False)

def createProduct(request):
	path = sessionPath(request, '/create-product/')
	categories = list(Category.objects.all())
	imgList=[]
	if request.method == 'POST':
		name = request.POST.get('productName')
		price = request.POST.get('price')
		try:
			if request.POST.get('oldPrice') != None:
				oldPrice = request.POST.get('oldPrice')
			else:
				oldPrice=price  
		except:
			oldPrice = price
		description = request.POST.get('description')
		category = Category.objects.get(name = request.POST.get('category'))
		print(request.POST.get('subcategory'))
		try:
			subcategory = SubCategory.objects.get(id = int(request.POST.get('subcategory')), category=category)
		except:
			subcategory = None
		for i in range(1, 8):
			imgList.append(request.FILES.get('img'+str(i)))
		print(imgList)
		product, created = Product.objects.get_or_create(name=name, price=price, oldPrice=oldPrice, description=description, category=category, subcategory=subcategory, picture=imgList[0])
		if created:
			pictureList, created = PictureList.objects.get_or_create(product=product)
			pictureList.picture1 = imgList[1]
			pictureList.picture2 = imgList[2]
			pictureList.picture3 = imgList[3]
			pictureList.picture4 = imgList[4]
			pictureList.picture5 = imgList[5]
			pictureList.picture6 = imgList[6]
			pictureList.save()
			messages.success(request, ("Товар создан успешно!"))
			return redirect('/')
		else:
			messages.success(request, ("Товар уже существует!"))
			return redirect('product-page/'+str(product.id))
	data = cartData(request)
	cartItems = data['cartItems']
	order = data['order']
	items =  data['items']
	return render(request, 'create_product.html', {'categories': categories, 'cartItems': cartItems, 'order': order, 'items': items})

def createCategory(request):
	data = json.loads(request.body)
	catName=data['catName']

	print(catName)

	try:
		category = Category.objects.create(name=catName)
		return JsonResponse('Category successfully created!', safe = False)
	except:
		return JsonResponse('Something went wrong', safe = False)

def deleteCategory(request):
	data = json.loads(request.body)
	catName=data['catName']

	try:
		category = Category.objects.get(name=catName)
		category.delete()
		return JsonResponse('Category successfully deleted!', safe = False)
	except:
		return JsonResponse('Something went wrong', safe = False)

def createSubCategory(request):
	data = json.loads(request.body)
	catName=data['catName']
	subcatName=data['subcatName']

	try:
		category = Category.objects.get(name=catName)
		subCategory = SubCategory.objects.create(category=category, name=subcatName)
		return JsonResponse('Subcategory successfully created!', safe = False)
	except:
		return JsonResponse('Something went wrong', safe = False)

def deleteSubCategory(request):
	data = json.loads(request.body)
	catName=data['catName']
	subcatName=data['subcatName']

	try:
		category = Category.objects.get(name=catName)
		subCategory = SubCategory.objects.get(category=category, name=subcatName)
		subCategory.delete()
		return JsonResponse('Subcategory successfully deleted!', safe = False)
	except:
		return JsonResponse('Something went wrong', safe = False)

def create_product_ajax(request):
    data = json.loads(request.body)
    subcategories = None

    categories = list(Category.objects.all())

    for i in categories:
        if data['category'] == i.name :
            subcategories = [model_to_dict(i) for i in list(SubCategory.objects.filter(category=i))]
            break

    if subcategories == None :
        return JsonResponse('Something went wrong in categories!', safe=False)

    return JsonResponse({
        'category': data['category'],
        'subcategories': subcategories,
    }, safe=False)

def editProduct(request, id):
	path = sessionPath(request, '/edit-product/'+str(id))
	names = ['productName', 'price', 'description']
	modelNames = ['name', 'price', 'description']
	product = Product.objects.get(id=id)
	categories = list(Category.objects.all())
	pictures = PictureList.objects.get(product=product) 
	imgList=[getattr(pictures, 'picture' + str(i)) for i in range(1, 7)]
	if request.method == 'POST':

		for i, j in zip(names, modelNames):
			print(request.POST.get(i))
			setattr(product, j, request.POST.get(i))
		try:
			if request.POST.get('oldPrice') != None:
				setattr(product, 'oldPrice', request.POST.get('oldPrice'))
			else:
				setattr(product, 'oldPrice', request.POST.get('price'))  
		except:
			setattr(product, 'oldPrice', request.POST.get('price'))
		category = Category.objects.get(name = request.POST.get('category'))
		try:
			setattr(product, 'subcategory', SubCategory.objects.get(id = int(request.POST.get('subcategory')), category=category))
		except:
			setattr(product, 'subcategory', None)
		if request.FILES.get('img1'):
			product.picture = request.FILES.get('img1')
		for i in range(2, 8):
			image = request.FILES.get('img'+str(i))
			if image:
				setattr(pictures, 'picture' + str(i), image)
		product.save()
		pictures.save()
		messages.success(request, ("Товар успешно изменён!"))
		return redirect('/')
	data = cartData(request)
	cartItems = data['cartItems']
	order = data['order']
	items =  data['items']
	return render(request, 'edit_product.html', {'product': product, 'categories': categories, 'cartItems': cartItems, 'order': order, 'items': items, 'imgList': imgList})
