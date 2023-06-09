import json
from .models import * 
from django.template.defaulttags import register

def sessionPath(request, url) :

    try :
        next = request.session['next']
        request.session['next'] = request.session['path']
        request.session['path'] = url
    except :
        next = '/'
        request.session['next'] = url
        request.session['path'] = url

    return next

def cookieCart(request):

    try:
        cart = json.loads(request.COOKIES['cart'])
    except :
        cart = {}

    items = []
    order = {'get_cart_total': 0, 'get_cart_items': 0}
    cartItems = order['get_cart_items']

    for i in cart:
        try:
            cartItems += cart[i]['quantity']
            product = Product.objects.get(id=i)
            total = (product.price * cart[i]['quantity'])

            order['get_cart_total'] += total
            order['get_cart_items'] += cart[i]['quantity']

            item = {
                "product": {
                'id': product.id,
                'name': product.name,
                'price': product.price,
                'picture': {'url': product.picture.url,},
                },
                'quantity': cart[i]['quantity'],
                'get_total': total,
                }

            items.append(item)
        except:
            pass
    return {'cartItems': cartItems, 'order': order, 'items': items}

def cartData(request):
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer = customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else :
        cookieData = cookieCart(request)
        cartItems = cookieData['cartItems']
        order = cookieData['order']
        items = cookieData['items']
    return {'cartItems': cartItems, 'order': order, 'items': items}

def guestOrder(request, email):
    cookieData = cookieCart(request)
    items = cookieData['items']

    customer, created = User.objects.get_or_create(
        email = email, 
        )

    order, created = Order.objects.get_or_create(
        customer=customer,
        complete = False,
        )

    for i in items:
        product = Product.objects.get(id=i['product']['id'])

        orderItem, created = OrderItem.objects.get_or_create(
            product = product,
            order = order,
            )

        orderItem.quantity += i['quantity']
        orderItem.save()
    return customer, order

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)