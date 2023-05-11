function SubmitData() {
    var name = document.getElementById('floatingName').value
    var price = '$' + document.getElementById('inputPrice').value
    if (document.getElementById('oldPrice') !== null) {
        var oldPrice = '$' + document.getElementById('oldPrice').value
    } else {
        var oldPrice = null
    }
    var description = document.getElementById('description').value
    var category = document.getElementById('selectCategory').value
    var subcategory = document.getElementById('selectSubcategory').value
    var img1 = document.getElementById('img1').src
    var img2 = document.getElementById('img2').src
    var img3 = document.getElementById('img3').src
    var img4 = document.getElementById('img4').src
    var img5 = document.getElementById('img5').src
    var img6 = document.getElementById('img6').src
    var img7 = document.getElementById('img7').src
    console.log(img7)
    if (name!="" && price !="$" && description!="" && category!="") {
        for (var i = 1; i < 8; i++) {
            element = document.getElementById('img'+String(i))
            if (element.src != "/static/product/add_image1.png") {
                var but = document.getElementById('submit-hidden')
                but.click()
                break
            }
        alert('You must fille all the fields and add at least 1 picture!')
        } 
    } else {
        alert('You must fille all the fields and add at least 1 picture!')
    }
}

function removeOptions(selectElement, initial) {
    console.log('i`M HERE', selectElement)
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

    var e = document.getElementById('selectCategory')
    var selectedOption = e.value
    if (selectedOption == "") {
        removeOptions(document.getElementById('selectCategory'), "Select category")
        removeOptions(document.getElementById('selectSubcategory'), "Select Subcategory")
        return
    } else if (selectedOption == "Select category") {
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
            var select = document.getElementById("selectSubcategory");
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

var initialSrc = "/static/product/add_image1.png";

var input = document.getElementsByClassName('input-photo')[0];


function PhotoSection(el, evt, id) {
    var tgt = evt.target || window.event.srcElement, files = tgt.files;
    var clone = el.cloneNode(true)

    el.id = 'input' + id
    el.name = id

    

    // FileReader support
    if (FileReader && files && files.length) {
        var fr = new FileReader();
        fr.onload = function () {
            var sliderMainImage = document.getElementById("imgPreview");
            sliderMainImage.src = fr.result;
            var sliderImage = document.getElementById(id);
            console.log(id)
            sliderImage.src = fr.result;
        }    
        fr.readAsDataURL(files[0]);
    }
    
    // Not supported
    else {
        console.log('Our browser does not support File Reader ((Whatever that means))')
    }

    console.log(clone)
    el.after(clone)
    document.getElementById('hiddenform').append(el)
    document.getElementById(id).dataset.hasimg='true'
    document.getElementsByClassName('overlay')[0].innerHTML += '<button type="button" class="btn btn-danger" id="' + 'd' + id + '" onclick="RemoveImage(this.id)">Remove Image</button>';
    document.getElementById('photo1').remove()
}

function RemoveImage(id) {
    var targetId = id.slice(1, id.length)
    console.log(targetId)
    var sliderMainImage = document.getElementById("imgPreview");
    sliderMainImage.src = initialSrc;
    var sliderImage = document.getElementById(targetId);
    sliderImage.src = initialSrc;
    document.getElementById(targetId).dataset.hasimg='false'
    document.getElementById('input' + targetId).remove()
    document.getElementById('d' + targetId).remove()
    document.getElementById('photo1').remove()
    document.getElementById('a' + targetId).classList.remove('hidden')
    document.getElementById(id).remove()
}

function AddField(id) {
    var targetId = id.slice(1, id.length)
    console.log(targetId)
    document.getElementById(id).classList.add('hidden')
    var inner = '<input class="input-photo form-control" type="file" name="photograph" id="photo1" required="true" data-imgid="' + targetId + '" onchange="PhotoSection(this, event, this.dataset.imgid)" placeholder="/static{{ product.picture.url }}"/>'
    document.getElementsByClassName('overlay')[0].innerHTML += inner;
}

function AddDiscount() {
    var container = document.getElementsByClassName('discount')[0];
    container.innerHTML = '<span class="input-group-text" id="basic-addon1">$</span><input type="text" class="form-control" placeholder="Old Price" aria-label="Old Price" aria-describedby="basic-addon1" id="oldPrice" name="oldPrice">'
    document.getElementsByClassName('hide-discount')[0].classList.remove('hidden')
    var oldPrice = document.getElementsByClassName('old-price')[0].placeholder = 'New Price';
}

function RemoveDiscount() {
    var container = document.getElementsByClassName('discount')[0];
    container.innerHTML = '<button type="button" class="btn btn-info" onclick="AddDiscount()">Add a discount</button>'
    document.getElementsByClassName('hide-discount')[0].classList.add('hidden')
    var oldPrice = document.getElementsByClassName('old-price')[0].placeholder = 'Price';
}

function ShowSubcategory() {
    var subcatDiv=document.getElementById('subcategory')
    var catBut=document.getElementById('category')
    if (document.getElementById('selectCategory').value=="Select category") {
        subcatDiv.classList.add('hidden')
        catBut.classList.remove('hidden')
        document.getElementById('delcategory').classList.add('hidden')
    } else {
        subcatDiv.classList.remove('hidden')
        catBut.classList.add('hidden')
        document.getElementById('delcategory').classList.remove('hidden')
    }
    populate_list();
}

function AddCategory() {
    document.getElementById('categorydiv').classList.add('hidden')
    document.getElementById('categorynameform').classList.remove('hidden')
}

function CancelCategory() {
    document.getElementById('categorydiv').classList.remove('hidden')
    document.getElementById('categorynameform').classList.add('hidden')
}

function CreateCategory() {
    var url = '/create-category/'
    var catName = document.getElementById('categoryinput').value
    console.log(catName)
    if (catName == "") {
        alert('Add the name!')
        return
    } 

    fetch(url, {
        method: 'POST',
        headers:{
            'Content-Type':'application/json',
            'X-CSRFToken': csrftoken,
        },
        body:JSON.stringify({'catName': catName,})
    })

    .then((response) => {
        return response.json();
    })

    .then((data) => {
        console.log('data:', data)
        location.reload()
    });
}

function DeleteCategory() {
    var url = '/delete-category/'
    var catName = document.getElementById('categoryinput').value 

    fetch(url, {
        method: 'POST',
        headers:{
            'Content-Type':'application/json',
            'X-CSRFToken': csrftoken,
        },
        body:JSON.stringify({'catName': catName,})
    })

    .then((response) => {
        return response.json();
    })

    .then((data) => {
        console.log('data:', data)
        location.reload()
    });
}

function AddSubCategory() {
    document.getElementById('subcategory').classList.add('hidden')
    document.getElementById('subcategorynameform').classList.remove('hidden')
}

function CancelSubCategory() {
    document.getElementById('subcategory').classList.remove('hidden')
    document.getElementById('subcategorynameform').classList.add('hidden')
}

function CreateSubCategory() {
    var url = '/create-subcategory/'
    var subcatName = document.getElementById('subcategoryinput').value
    var catName = document.getElementById('selectCategory').value 

    if (subcatName == "") {
        alert('Add the name!')
        return
    } 

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
        console.log('data:', data)
        location.reload()
    });
}

function DeleteSubCategory() {
    var url = '/delete-subcategory/'
    var subcatName = document.getElementById('subcategoryinput').value
    var catName = document.getElementById('selectCategory').value 

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
        console.log('data:', data)
        location.reload()
    });
}


function ShowDelSubcategory() {
    var subcatDiv=document.getElementById('subcategory')
    var subcatBut=document.getElementById('addsubcategorybut')
    if (document.getElementById('selectSubcategory').value=="Select Subcategory") {
        subcatBut.classList.remove('hidden')
        document.getElementById('delsubcategory').classList.add('hidden')
    } else {
        subcatBut.classList.add('hidden')
        document.getElementById('delsubcategory').classList.remove('hidden')
    }
}