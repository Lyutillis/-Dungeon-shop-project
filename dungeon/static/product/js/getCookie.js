function getToken(name) {
	let cookieValue = null;
	if (document.cookie && document.cookie !== '') {
		const cookies = document.cookie.split(';');
		for (var i = 0; i < cookies.length; i++) {
			const cookie = cookies[i].trim();
			// Does this cookie string begin with the name we want?
			if (cookie.substring(0, name.length + 1) === (name + '=')) {
				cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
				break;
			}
		}
	}
	return cookieValue;
}

function getCookie(name) {
	var cookieArr = document.cookie.split(';');

	for (var i = 0; i < cookieArr.length; i++) {
		var cookiePair = cookieArr[i].split('=');

		if (name == cookiePair[0].trim()) {
			return decodeURIComponent(cookiePair[1]);
		}
	}
	return null;
}

if (cart == undefined){
	cart = {}
	document.cookie ='cart=' + JSON.stringify(cart) + ";domain=;path=/"
}

var csrftoken = getToken('csrftoken');
var cart = JSON.parse(getCookie('cart'))