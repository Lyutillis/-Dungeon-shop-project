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

function clearFilter() {
    var subcatDiv=document.getElementById('subcategory')
    document.getElementById('goBut').classList.add('hidden')
    document.getElementById('clearBut').classList.add('hidden')
    subcatDiv.classList.add('hidden')
    document.getElementById('catselect').value="Category"
}

function ShowSubcategory() {
    var subcatDiv=document.getElementById('subcategory')
    if (document.getElementById('catselect').value=="Category") {
        subcatDiv.classList.add('hidden')
        document.getElementById('goBut').classList.add('hidden')
        document.getElementById('clearBut').classList.add('hidden')
    } else {
        subcatDiv.classList.remove('hidden')
        document.getElementById('goBut').classList.remove('hidden')
        document.getElementById('clearBut').classList.remove('hidden')
    }

    populate_list();
}

function removeOptions(selectElement, initial) {
    var i, L = selectElement.options.length - 1
    for(i=L; i >= 0; i--) {
        selectElement.remove(i)
    }

    var opt = document.createElement('option');
    opt.value=""
    opt.innerHTML=initial;
    selectElement.appendChild(opt)
}

function populate_list() {
    const url='/create-product-ajax/'
    const csrftoken=getToken('csrftoken');

    var e = document.getElementById('catselect')
    var selectedOption = e.value
    if (selectedOption == "") {
        removeOptions(document.getElementById('catselect'), "Category")
        removeOptions(document.getElementById('subcatselect'), "Subcategory")
        return
    } else if (selectedOption == "Category") {
        return   
    }
    
    // Send AJAX Request
    fetch(url, {
        method: 'POST',
        headers: {
            'X-CSRFToken': csrftoken,
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            "category": selectedOption,
        }),
    })
    .then((response) => response.json())
    .then((data) => {
        var select = document.getElementById("selectCategory");

        if (data.subcategories != null) {
            var select = document.getElementById("subcatselect");
            removeOptions(select, `All subcategories from ${data.category}`);
            for (var i = 0; i<=data.subcategories.length-1; i++){
                var opt = document.createElement('option');
                opt.value = data.subcategories[i]['id'];
                opt.innerHTML = data.subcategories[i]['name'];
                select.appendChild(opt);
            }
        }
        
    })
    .catch((error) => {
        console.error('Error:', error);
    });
}