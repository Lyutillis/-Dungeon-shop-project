if (user == 'AnonymousUser'){
    document.getElementById('form').classList.add("hidden");
    document.getElementById('login').classList.remove("hidden");
}

document.getElementById('star1').addEventListener('change', function(){
if (this.checked) {
    document.getElementById('user-send-disabled').classList.add('hidden')
    document.getElementById('user-send').classList.remove('hidden')
}
})

document.getElementById('star2').addEventListener('change', function(){
if (this.checked) {
    document.getElementById('user-send-disabled').classList.add('hidden')
    document.getElementById('user-send').classList.remove('hidden')
}
})

document.getElementById('star3').addEventListener('change', function(){
if (this.checked) {
    document.getElementById('user-send-disabled').classList.add('hidden')
    document.getElementById('user-send').classList.remove('hidden')
}
})

document.getElementById('star4').addEventListener('change', function(){
if (this.checked) {
    document.getElementById('user-send-disabled').classList.add('hidden')
    document.getElementById('user-send').classList.remove('hidden')
}
})

document.getElementById('star5').addEventListener('change', function(){
if (this.checked) {
    document.getElementById('user-send-disabled').classList.add('hidden')
    document.getElementById('user-send').classList.remove('hidden')
}
})


var replies = document.getElementsByClassName('replies')
var repl = replies[0].getElementsByClassName('reply')[0];
var hiderepl = replies[0].getElementsByClassName('reply-hide')[0];

for(let i = 0; i < replies.length; i++){
repl = replies[i].getElementsByClassName('reply')[0];
hiderepl = replies[i].getElementsByClassName('reply-hide')[0];

(function () { 
    repl.addEventListener('click', function(){
        console.log('Button', i, 'clicked');
        replies[i].getElementsByClassName('reply')[0].classList.add("hidden");
        replies[i].getElementsByClassName('reply-hide')[0].classList.remove("hidden");
        if (user != 'AnonymousUser'){
            replies[i].getElementsByClassName('reply-form')[0].classList.remove("hidden");
        }
        replies[i].getElementsByClassName('reply-comments')[0].classList.remove("hidden");
        return 0;
    })

    hiderepl.addEventListener('click', function(){
        console.log('Hide-Button', i, 'clicked'); 
        replies[i].getElementsByClassName('reply')[0].classList.remove("hidden");
        replies[i].getElementsByClassName('reply-hide')[0].classList.add("hidden");
        if (user != 'AnonymousUser'){
            replies[i].getElementsByClassName('reply-form')[0].classList.add("hidden");
        }
        replies[i].getElementsByClassName('reply-comments')[0].classList.add("hidden");
        return 0;
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