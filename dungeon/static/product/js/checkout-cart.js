var checkoutBtns = document.getElementsByClassName('update-cart-checkout')

checkoutBtns[0].addEventListener('click', function(){
	var productId = this.dataset.product
	var action = this.dataset.action
	console.log('productId:', productId, 'action:', action)

	console.log('USER', user)
	if(user=='AnonymousUser'){
		checkoutAddCookieItem(productId, action)
	}else{
		checkoutUpdateUserOrder(productId, action)
	}
})

function checkoutAddCookieItem(productId, action){

	if (action=='add'){
		if (cart[productId] == undefined){
			cart[productId] = {'quantity': 1}
		} else {
			cart[productId]['quantity'] += 1
		}
	}

	if (action=='remove'){
		cart[productId]['quantity'] -= 1

		if (cart[productId]['quantity'] <= 0){
			console.log('Item should be deleted')
			delete cart[productId]
		}
	}
	console.log('Cart:', cart)
	document.cookie = 'cart=' + JSON.stringify(cart) + ';domain=;path=/' 
	location.replace('/checkout/')
}

function checkoutUpdateUserOrder(productId, action){
		var url = '/update-item/'

		fetch(url, {
			method: 'POST',
			headers:{
				'Content-Type':'application/json',
				'X-CSRFToken': csrftoken,
			},
			body:JSON.stringify({'productId': productId, 'action': action})
		})

	.then((response) => {
		return response.json();
	})

	.then((data) => {
		location.replace('/checkout/')
	});
}