function Continue(e){
    var address = document.getElementById('address').value;
    var city = document.getElementById('city').value;
    var zipCode = document.getElementById('zipCode').value;
    if (address != '' && city!='' && zipCode!='') {
        console.log('Form Submitted...')
        document.getElementById('form-button').classList.add("hidden");
        document.getElementById('payment-info').classList.remove("hidden");
    }
}

if (user == 'AnonymousUser'){
    document.getElementById('user-info').classList.remove('hidden')
}


var form = document.getElementById('form')
form.addEventListener('submit', function(e){
    e.preventDefault()
})

function submitFormData(){
    console.log('Paymnet button clicked')

    var userFormData = {
        'name': null,
        'email': null,
        'total': total,
    }

    var shippingInfo = {
        'address': null,
        'city': null,
        'state': null,
        'zipcode': null,
    }

    shippingInfo.address = form.address.value
    shippingInfo.city = form.city.value
    shippingInfo.zipcode = form.zipcode.value
    console.log('Shipping info collected')

    if (user == 'AnonymousUser'){
        userFormData.name = form.name.value
        userFormData.email = form.email.value
    }
    console.log('Anon user checked')

    var url = '/process-order/'
    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type':'application/json',
            'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify({'form': userFormData, 'shipping': shippingInfo}),
    })

    .then((response) => response.json())

    .then((data) => {
        console.log('Success:', data);
        alert('Transaction completed');

        cart = {}
        document.cookie = 'cart=' + JSON.stringify(cart) + ";domain=;path=/"

        window.location.href = "/"
    })
    console.log('Data')
}