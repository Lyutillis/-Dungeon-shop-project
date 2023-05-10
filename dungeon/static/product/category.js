function ShowFields(id) {
    var cont = document.getElementById(id).parentNode
    cont.getElementsByClassName('btn')[0].classList.add('hidden')
    cont.getElementsByClassName('btn')[1].classList.add('hidden')
    cont.getElementsByClassName('btn')[2].classList.remove('hidden')
    document.getElementById('name' + id).classList.remove('hidden')
    document.getElementById('p' + id).classList.add('hidden')
}

function HideFields(id) {
    id = id.slice(1, id.length)
    var url='/save-subcategory/'
    var name = document.getElementById('name'+id).value
    
    fetch(url + new URLSearchParams({id: id}), {
        method: 'POST',
        headers:{
            'Content-Type':'application/json',
            'X-CSRFToken': csrftoken,
        },
        body:JSON.stringify({'name': name,})
    })

    .then((response) => {
        return response.json();
    })

    .then((data) => {
        var cont = document.getElementById(id).parentNode
        cont.getElementsByClassName('btn')[0].classList.remove('hidden')
        cont.getElementsByClassName('btn')[1].classList.remove('hidden')
        cont.getElementsByClassName('btn')[2].classList.add('hidden')
        document.getElementById('name' + id).classList.add('hidden')
        document.getElementById('p' + id).classList.remove('hidden')
        location.reload()
    });
}

function CreateSub(id) {
    id = id.slice(1, id.length)
    var url='/create-subcategory/'
    var catName=document.getElementById('catfield').placeholder
    var subcatName = document.getElementById('newname').value
    
    fetch(url, {
        method: 'POST',
        headers:{
            'Content-Type':'application/json',
            'X-CSRFToken': csrftoken,
        },
        body:JSON.stringify({'catName': catName, 'subcatName': subcatName,})
    })

    .then((response) => {
        return response.json();
    })

    .then((data) => {
        location.reload()
    });
}

function ChangeName(id) {
    id = id.slice(2, id.length)
    var url='/save-category/'
    var name = document.getElementById('catfield').value
    
    fetch(url + new URLSearchParams({id: id}), {
        method: 'POST',
        headers:{
            'Content-Type':'application/json',
            'X-CSRFToken': csrftoken,
        },
        body:JSON.stringify({'name': name,})
    })

    .then((response) => {
        return response.json();
    })

    .then((data) => {
        location.reload()
    });
}