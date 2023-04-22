const sliderMainImage = document.getElementById("imgPreview"); //product container image
const sliderImageList = document.getElementsByClassName("image-list"); // image thumblian group selection
const mainInput = document.getElementsByClassName("overlay")[0]; //product container image
console.log(sliderImageList);
console.log(sliderMainImage);
console.log(mainInput);

if (sliderImageList.length >= 1) {sliderImageList[0].onmouseover = function(){
    sliderMainImage.src = sliderImageList[0].src;
    mainInput.innerHTML = '<input class="input-photo" type="file" name="photograph" id="photo1" required="true" onchange="PhotoSection1(event)" />';
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
    mainInput.innerHTML = '<input class="input-photo" type="file" name="photograph" id="photo1" required="true" onchange="PhotoSection2(event)" />';
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
    mainInput.innerHTML = '<input class="input-photo" type="file" name="photograph" id="photo1" required="true" onchange="PhotoSection3(event)" />';
    document.getElementsByClassName('image-list')[2].classList.add("slider-border");
    for(i = 0; i < sliderImageList.length; i++){
        if (i != 2) {
            document.getElementsByClassName('image-list')[i].classList.remove("slider-border");
        }
    }
};}

if (sliderImageList.length >= 4){sliderImageList[3].onmouseover = function(){
    sliderMainImage.src = sliderImageList[3].src;
    mainInput.innerHTML = '<input class="input-photo" type="file" name="photograph" id="photo1" required="true" onchange="PhotoSection4(event)" />';
    document.getElementsByClassName('image-list')[3].classList.add("slider-border");
    for(i = 0; i < sliderImageList.length; i++){
        if (i != 3) {
            document.getElementsByClassName('image-list')[i].classList.remove("slider-border");
        }
    }
};}

if (sliderImageList.length >= 5){sliderImageList[4].onmouseover = function(){
    sliderMainImage.src = sliderImageList[4].src;
    mainInput.innerHTML = '<input class="input-photo" type="file" name="photograph" id="photo1" required="true" onchange="PhotoSection5(event)" />';
    document.getElementsByClassName('image-list')[4].classList.add("slider-border");
    for(i = 0; i < sliderImageList.length; i++){
        if (i != 4) {
            document.getElementsByClassName('image-list')[i].classList.remove("slider-border");
        }
    }
};}

if (sliderImageList.length >= 6){sliderImageList[5].onmouseover = function(){
    sliderMainImage.src = sliderImageList[5].src;
    mainInput.innerHTML = '<input class="input-photo" type="file" name="photograph" id="photo1" required="true" onchange="PhotoSection6(event)" />';
    document.getElementsByClassName('image-list')[5].classList.add("slider-border");
    for(i = 0; i < sliderImageList.length; i++){
        if (i != 5) {
            document.getElementsByClassName('image-list')[i].classList.remove("slider-border");
        }
    }
};}

if (sliderImageList.length == 7){sliderImageList[6].onmouseover = function(){
    sliderMainImage.src = sliderImageList[6].src;
    mainInput.innerHTML = '<input class="input-photo" type="file" name="photograph" id="photo1" required="true" onchange="PhotoSection7(event)" />';
    document.getElementsByClassName('image-list')[6].classList.add("slider-border");
    for(i = 0; i < sliderImageList.length; i++){
        if (i != 6) {
            document.getElementsByClassName('image-list')[i].classList.remove("slider-border");
        }
    }
};}