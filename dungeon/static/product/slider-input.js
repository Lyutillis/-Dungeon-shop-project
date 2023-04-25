const sliderMainImage = document.getElementById("imgPreview"); //product container image
const sliderImageList = document.getElementsByClassName("image-list"); // image thumblian group selection
const mainInput = document.getElementsByClassName("overlay")[0]; //product container image
console.log(sliderImageList);
console.log(sliderMainImage);
console.log(mainInput);

if (sliderImageList.length >= 1) {sliderImageList[0].onmouseover = function(){
    sliderMainImage.src = sliderImageList[0].src;
    mainInput.innerHTML = '<input class="input-photo" type="file" name="photograph" id="photo1" required="true" data-imgid="img1" onchange="PhotoSection(event, this.dataset.imgid)" /><button type="button" class="btn btn-danger" id="dimg1" onclick="RemoveImage(this.id)">Remove Image</button>';
    document.getElementsByClassName('image-list')[0].classList.add("slider-border");
    for(i = 0; i < sliderImageList.length; i++){
        if (i != 0) {
            document.getElementsByClassName('image-list')[i].classList.remove("slider-border");
        }
    }
};
}

if (sliderImageList.length >= 2) {sliderImageList[1].onmouseover = function(){
    sliderMainImage.src = sliderImageList[1].src;
    mainInput.innerHTML = '<input class="input-photo" type="file" name="photograph" id="photo1" required="true" data-imgid="img2" onchange="PhotoSection(event, this.dataset.imgid)" /><button type="button" class="btn btn-danger" id="dimg2" onclick="RemoveImage(this.id)">Remove Image</button>';
    document.getElementsByClassName('image-list')[1].classList.add("slider-border");
    for(i = 0; i < sliderImageList.length; i++){
        if (i != 1) {
            document.getElementsByClassName('image-list')[i].classList.remove("slider-border");
        }
    }
};
}

if (sliderImageList.length >= 3){sliderImageList[2].onmouseover = function(){
    sliderMainImage.src = sliderImageList[2].src;
    mainInput.innerHTML = '<input class="input-photo" type="file" name="photograph" id="photo1" required="true" data-imgid="img3" onchange="PhotoSection(event, this.dataset.imgid)" /><button type="button" class="btn btn-danger" id="dimg3" onclick="RemoveImage(this.id)">Remove Image</button>';
    document.getElementsByClassName('image-list')[2].classList.add("slider-border");
    for(i = 0; i < sliderImageList.length; i++){
        if (i != 2) {
            document.getElementsByClassName('image-list')[i].classList.remove("slider-border");
        }
    }
};}

if (sliderImageList.length >= 4){sliderImageList[3].onmouseover = function(){
    sliderMainImage.src = sliderImageList[3].src;
    mainInput.innerHTML = '<input class="input-photo" type="file" name="photograph" id="photo1" required="true" data-imgid="img4" onchange="PhotoSection(event, this.dataset.imgid)" /><button type="button" class="btn btn-danger" id="dimg4" onclick="RemoveImage(this.id)">Remove Image</button>';
    document.getElementsByClassName('image-list')[3].classList.add("slider-border");
    for(i = 0; i < sliderImageList.length; i++){
        if (i != 3) {
            document.getElementsByClassName('image-list')[i].classList.remove("slider-border");
        }
    }
};}

if (sliderImageList.length >= 5){sliderImageList[4].onmouseover = function(){
    sliderMainImage.src = sliderImageList[4].src;
    mainInput.innerHTML = '<input class="input-photo" type="file" name="photograph" id="photo1" required="true" data-imgid="img5" onchange="PhotoSection(event, this.dataset.imgid)" /><button type="button" class="btn btn-danger" id="dimg5" onclick="RemoveImage(this.id)">Remove Image</button>';
    document.getElementsByClassName('image-list')[4].classList.add("slider-border");
    for(i = 0; i < sliderImageList.length; i++){
        if (i != 4) {
            document.getElementsByClassName('image-list')[i].classList.remove("slider-border");
        }
    }
};}

if (sliderImageList.length >= 6){sliderImageList[5].onmouseover = function(){
    sliderMainImage.src = sliderImageList[5].src;
    mainInput.innerHTML = '<input class="input-photo" type="file" name="photograph" id="photo1" required="true" data-imgid="img6" onchange="PhotoSection(event, this.dataset.mgid)" /><button type="button" class="btn btn-danger" id="dimg6" onclick="RemoveImage(this.id)">Remove Image</button>';
    document.getElementsByClassName('image-list')[5].classList.add("slider-border");
    for(i = 0; i < sliderImageList.length; i++){
        if (i != 5) {
            document.getElementsByClassName('image-list')[i].classList.remove("slider-border");
        }
    }
};}

if (sliderImageList.length == 7){sliderImageList[6].onmouseover = function(){
    sliderMainImage.src = sliderImageList[6].src;
    mainInput.innerHTML = '<input class="input-photo" type="file" name="photograph" id="photo1" required="true" data-imgid="img7" onchange="PhotoSection(event, this.dataset.imgid)" /><button type="button" class="btn btn-danger" id="dimg7" onclick="RemoveImage(this.id)">Remove Image</button>';
    document.getElementsByClassName('image-list')[6].classList.add("slider-border");
    for(i = 0; i < sliderImageList.length; i++){
        if (i != 6) {
            document.getElementsByClassName('image-list')[i].classList.remove("slider-border");
        }
    }
};}