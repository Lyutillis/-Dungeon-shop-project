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
	data = json.loads(request.body)
	customer = request.user

	total = float(data['form']['total'])

	transaction_id = datetime.datetime.now().timestamp()

	order, created = Order.objects.get_or_create(customer=customer, complete=False)
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
	from user.models import WishList
	path = sessionPath(request, '/product-page/' + str(id))
	data = cartData(request)
	cartItems = data['cartItems']
	if request.user.is_authenticated :
		wishlist = [i.product for i in WishList.objects.filter(user=request.user)]
	else :
		wishlist = None

	product=Product.objects.get(id=id)
	piclist=PictureList.objects.get(product=product)
	pictures=[getattr(piclist, 'picture'+str(i)) if getattr(piclist, 'picture'+str(i)) else None for i in range(1,7)]
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

	return render(request, 'product_page.html', {'wishlist': wishlist, 'pictures': pictures, 'product': product, 'cartItems': cartItems, 'comments': comments, 'replies': replies, 'rating': round(rating.overall), 'quantity': quantity,})

def update_item(request):
	data = json.loads(request.body)

	productId=data['productId']
	action=data['action']

	customer = request.user
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
		body = request.POST.get('content')
		product = Product.objects.get(id=id)
		comment = Comment.objects.create(customer = request.user, product = product, body = body, rating = int(rate[0]))		
		rating, created = Rating.objects.get_or_create(product=product)
		rating.quantity += 1
		rating.stars += int(rate[0])
		rating.overall = rating.stars/rating.quantity
		rating.save()
		messages.success(request, ("Комментарий успешно добавлен!"))
		return redirect(path)
	return redirect(path)

def publishReply(request, id):
	path = sessionPath(request, '/product-page/' + str(id))
	if request.method == 'POST' :
		body = request.POST.get('content')
		comment = Comment.objects.get(id=id)
		replycomment = ReplyComment.objects.create(customer = request.user, body = body)
		reply = Reply.objects.create(comment=comment, reply=replycomment)
		messages.success(request, ("Reply успешно добавлен!"))
		return redirect(path)
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

	user = User.objects.get(id = int(userId))

	if action == 'True' :
		user.is_superuser = True
	elif action == 'False' :
		user.is_superuser = False

	user.save()

	return JsonResponse('User permissions were updated!', safe = False)

def updatePermissionStaff(request):
	data = json.loads(request.body)
	userId=data['userId']
	action=data['action']

	user = User.objects.get(id = int(userId))

	if action == 'True' :
		user.is_staff = True
	elif action == 'False' :
		user.is_staff = False

	user.save()

	return JsonResponse('User permissions were updated!', safe = False)

def createProduct(request):
	path = sessionPath(request, '/create-product/')
	categories = list(Category.objects.all())
	if request.method == 'POST':
		name = request.POST.get('productName')
		price = request.POST.get('price')
		try:
			if request.POST.get('oldPrice') :
				oldPrice = request.POST.get('oldPrice')
			else:
				oldPrice=price  
		except:
			oldPrice = price
		description = request.POST.get('description')
		try:
			category = Category.objects.get(name = request.POST.get('category'))
		except:
			category=None
		try:
			subcategory = SubCategory.objects.get(id = int(request.POST.get('subcategory')))
		except:
			subcategory = None
		imgList=[request.FILES.get('img'+str(i)) for i in range(1,8)]
		product, created = Product.objects.get_or_create(name=name, price=price, oldPrice=oldPrice, description=description, category=category, subcategory=subcategory, picture=imgList[0])
		if created:
			pictureList, created = PictureList.objects.get_or_create(product=product)
			for i in range(1, 7) :
				setattr(pictureList, 'picture' + str(i), imgList[i])
			pictureList.save()
			messages.success(request, ("Товар создан успешно!"))
			return redirect('/')
		else:
			messages.success(request, ("Товар уже существует!"))
			return redirect('product-page/'+str(product.id))
	data = cartData(request)
	cartItems = data['cartItems']
	return render(request, 'create_product.html', {'categories': categories, 'cartItems': cartItems,})

def createCategory(request):
	data = json.loads(request.body)
	catName=data['catName']

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
	if subcatName != "" and subcatName :
		try:
			category = Category.objects.get(name=catName)
			subCategory = SubCategory.objects.create(category=category, name=subcatName)
			return JsonResponse('Subcategory successfully created!', safe = False)
		except:
			return JsonResponse('Something went wrong', safe = False)
	messages.success(request, ('Can`t set empty field'))
	return JsonResponse('Empty field!', safe = False)

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

def populate_list_ajax(request):
	data = json.loads(request.body)

	category = Category.objects.get(name=data['category'])

	try:
		subcategories = [model_to_dict(i) for i in list(SubCategory.objects.filter(category=category))]
	except:
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

		if request.POST.get('oldPrice') != None:
			setattr(product, 'oldPrice', request.POST.get('oldPrice'))
		else:
			setattr(product, 'oldPrice', request.POST.get('price'))  
		
		setattr(product, 'oldPrice', request.POST.get('price'))

		category = Category.objects.get(name = request.POST.get('category'))

		try:
			setattr(product, 'subcategory', SubCategory.objects.get(id = int(request.POST.get('subcategory'))))
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
	messages.success(request, ('Something went wrong!'))
	return render(request, 'edit_product.html', {'product': product, 'categories': categories, 'cartItems': cartItems, 'imgList': imgList})

def deleteProduct(request, id):
	product=Product.objects.get(id=id)
	product.delete()
	return redirect('/')

def categoryFilter(request):
	path = sessionPath(request, '/')
	data = cartData(request)

	if request.method == 'GET':
		try:
			category = Category.objects.get(name=request.GET.get('category'))
		except :
			category = None

		try:
			subcategory = SubCategory.objects.get(name=request.GET.get('subcategory'))
		except:
			subcategory = None

		if not subcategory :
			if not category :
				messages.success(request, ('You didn`t choose any category'))
				return redirect('/')
			else:
				product_list = list(Product.objects.filter(category=category))
		else:
			product_list = list(Product.objects.filter(category=category, subcategory=subcategory))
		
		return render(request, 'homepage.html', {'product_list':product_list, 'cartItems': data['cartItems'], 'categories': list(Category.objects.all())})

def categoryEdit(request):
	path = sessionPath(request, '/category-edit/')
	data = cartData(request)
	categories=list(Category.objects.all())
	subcategories = {}
	for i in categories:
		subcategories.update({i.name:list(SubCategory.objects.filter(category=i))})

	return render(request, 'category-edit.html', {'categories': categories, 'subcategories': subcategories, 'cartItems': data['cartItems'],})

def category(request, id):
	path = sessionPath(request, '/category/'+str(id))
	data = cartData(request)
	category=Category.objects.get(id=id)
	subcategories=list(SubCategory.objects.filter(category=category))
	return render(request, 'category.html', {'category': category, 'subcategories': subcategories, 'cartItems': data['cartItems'],})

def categoryDelete(request, id):
	category = Category.objects.get(id = id)
	category.delete()
	return redirect('/category-edit/')

def subcategoryDelete(request, id):
	subcategory = SubCategory.objects.get(id = id)
	catId = subcategory.category.id
	subcategory.delete()
	return redirect('/category/' + str(catId))

def subcategorySave(request, id):
	if request.method == "POST":
		data = json.loads(request.body)
		subcategory = SubCategory.objects.get(id=id)
		if name :
			subcategory.name = data['name']
			subcategory.save()
		return JsonResponse({
    	}, safe=False)

def categorySave(request, id):
	if request.method == "POST":
		data = json.loads(request.body)
		category = Category.objects.get(id=id)
		if name :
			category.name = data['name']
			category.save()
		return JsonResponse({
    	}, safe=False)

def searchView(request):
	context={}
	path = sessionPath(request, '/')
	data = cartData(request)
	context['cartItems'] = data['cartItems']
	context['categories'] = list(Category.objects.all())
	if request.method=='GET':
		query=request.GET.get('query')
		products = list(Product.objects.filter(name__icontains=query))
		if products: 
			context['product_list']=products
			messages.success(request, ('Search successfull!'))
			return render(request, 'homepage.html', context)
		else:
			context['product_list']=products
			context['search']=True
			messages.success(request, ('Search wasn`t successfull!'))
			return render(request, 'homepage.html', context)
	messages.success(request, ('Something went wrong'))
	return redirect('/')

def categoryLink(request, category):
	path = sessionPath(request, '/')
	data = cartData(request)

	try:
		category = Category.objects.get(name=category)
	except :
		category = None
		messages.success(request, ('You didn`t choose any category'))
		return redirect('/')
	
	product_list = list(Product.objects.filter(category=category))

	return render(request, 'homepage.html', {'product_list':product_list, 'cartItems': data['cartItems'], 'categories': list(Category.objects.all())})

def subcategoryLink(request, category, subcategory):
	path = sessionPath(request, '/')
	data = cartData(request)

	try:
		category = Category.objects.get(name=category)
	except :
		category = None

	try:
		subcategory = SubCategory.objects.get(name=subcategory)
	except:
		subcategory = None

	if not subcategory :
		if not category  :
			messages.success(request, ('You didn`t choose any category'))
			return redirect('/')
		else:
			product_list = list(Product.objects.filter(category=category))
	else:
		product_list = list(Product.objects.filter(category=category, subcategory=subcategory))
		
	return render(request, 'homepage.html', {'product_list':product_list, 'cartItems': data['cartItems'], 'categories': list(Category.objects.all())})

def orders(request):
	path = sessionPath(request, '/')
	data = cartData(request)

	user = request.user
	if user.is_authenticated:
		order=list(Order.objects.filter(customer=user))
		items=[]
		for i in order:
			items.extend(list(OrderItem.objects.filter(order=i)))
	else:
		items=[]
	return render(request, 'orders.html', {'items': items, 'cartItems': data['cartItems']})