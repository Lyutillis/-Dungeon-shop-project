function AlterFields() {
    var container = document.getElementById('cont')
    document.getElementById('imgcont').innerHTML += '<input id="el1" class="form-control" type="file" id="formFile" name="image" onchange="SetPhoto(this, event)">'
    document.getElementById('username').classList.add('hidden')
    document.getElementById('email').classList.add('hidden')
    document.getElementById('alterBut').classList.add('hidden')
    container.innerHTML += '<div id="el2" class="form-floating mb-3"><input type="text" class="form-control" id="floatingInputGroup1" placeholder="Username" value="{{ user.username }}" name="username"><label for="floatingInputGroup1">Username</label></div>'
    container.innerHTML += '<div id="el3" class="form-floating mb-3"><input type="email" class="form-control" id="floatingInput" placeholder="name@example.com" value="{{ user.email }}" name="email"><label for="floatingInput">Email address</label></div>'
    container.innerHTML += '<button id="el4" type="submit" class="btn btn-info btn-rounded btn-lg mx-3">Save</button>'
    container.innerHTML += '<button id="el5" type="button" class="btn btn-danger btn-rounded btn-lg mx-3" onclick=Cancel()>Cancel</button>'
}

function SetPhoto(el, evt) {
    var tgt = evt.target || window.event.srcElement, files = tgt.files;

    // FileReader support
    if (FileReader && files && files.length) {
        var fr = new FileReader();
        fr.onload = function () {
            var MainImage = document.getElementById("mainimg");
            MainImage.src = fr.result;
        }    
        fr.readAsDataURL(files[0]);
    }
    
    // Not supported
    else {
        console.log('Our browser does not support File Reader ((Whatever that means))')
    }
}

function Cancel() {
    var container = document.getElementById('cont')
    document.getElementById('username').classList.remove('hidden')
    document.getElementById('email').classList.remove('hidden')
    document.getElementById('alterBut').classList.remove('hidden')
    document.getElementById('imgcont').removeChild(document.getElementById('el1'))
    container.removeChild(document.getElementById('el2'))
    container.removeChild(document.getElementById('el3'))
    container.removeChild(document.getElementById('el4'))
    container.removeChild(document.getElementById('el5'))
}
