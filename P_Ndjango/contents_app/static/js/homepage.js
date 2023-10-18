var images = [

]

var imageArea = document.querySelector(".image_area");
var currentIndex = 0;
var delay = 3000;

function nextImage(){
    if (currentIndex >= images.length) {
        currentIndex = 0;
    }

    imageArea.innerHTML = "";

    var imgElement = document.createElement("img");
    imgElement.src = images[currentIndex];
    imgElement.alt = "Image";
    imgElement.classList.add("image_item");

    imageArea.appendChild(imgElement);

    currentIndex++;
}