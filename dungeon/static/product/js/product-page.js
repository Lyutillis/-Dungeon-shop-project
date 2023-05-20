var replies = document.getElementsByClassName('replies')
var repl = replies[0].getElementsByClassName('reply')[0];
var hiderepl = replies[0].getElementsByClassName('reply-hide')[0];

if (user == 'AnonymousUser'){
    document.getElementById('form').classList.add("hidden");
    document.getElementById('login').classList.remove("hidden");
}

for (let i=1; i<=5; i++) {
    document.getElementById('star'+ i.toString()).addEventListener('change', function(){
        if (this.checked) {
            document.getElementById('user-send-disabled').classList.add('hidden')
            document.getElementById('user-send').classList.remove('hidden')
        }
        })
}

for(let i = 0; i < replies.length; i++){
    repl = replies[i].getElementsByClassName('reply')[0];
    hiderepl = replies[i].getElementsByClassName('reply-hide')[0];

    (function () { 
        repl.addEventListener('click', function(){
            replies[i].getElementsByClassName('reply')[0].classList.add("hidden");
            replies[i].getElementsByClassName('reply-hide')[0].classList.remove("hidden");
            if (user != 'AnonymousUser'){
                replies[i].getElementsByClassName('reply-form')[0].classList.remove("hidden");
            }
            replies[i].getElementsByClassName('reply-comments')[0].classList.remove("hidden");
            return;
        })

        hiderepl.addEventListener('click', function(){
            replies[i].getElementsByClassName('reply')[0].classList.remove("hidden");
            replies[i].getElementsByClassName('reply-hide')[0].classList.add("hidden");
            if (user != 'AnonymousUser'){
                replies[i].getElementsByClassName('reply-form')[0].classList.add("hidden");
            }
            replies[i].getElementsByClassName('reply-comments')[0].classList.add("hidden");
            return;
        })
    }());
}

function hideOnEmpty(element, value) {
    var doc = element.parentNode.parentNode;
    var button = null;

    if (value !== '') {
        button = doc.getElementsByClassName('send-disabled')[0].classList.add('hidden')
        button = doc.getElementsByClassName('send')[0].classList.remove('hidden') 
    } else {
        button = doc.getElementsByClassName('send')[0].classList.add('hidden')
        button = doc.getElementsByClassName('send-disabled')[0].classList.remove('hidden') 
    }

}

function AddWishlist(id){
    var url='/add-to-wishlist/'

    if (user == 'AnonymousUser'){
        alert("You need to login or register to add items to wishlist")
        return
    }
    fetch(url, {
        method: 'POST',
        headers: {
            'X-CSRFToken': csrftoken,
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            "product": id,
        }),
    })

    .then((response) => response.json())
    .then((data) => {
        location.reload()
    })
    .catch((error) => {
        console.error('Error:', error);
    });
}

function RemoveWishlist(id) {
    var url='/remove-from-wishlist/'

    if (user == 'AnonymousUser'){
        alert("You need to login or register to add items to wishlist")
        return
    }

    fetch(url, {
        method: 'POST',
        headers: {
            'X-CSRFToken': csrftoken,
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            "product": id,
        }),
    })

    .then((response) => response.json())
    .then((data) => {
        location.reload()
    })
    .catch((error) => {
        console.error('Error:', error);
    });
}