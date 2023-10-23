function previewImage() {
    var preview = document.getElementById('imagePreview');
    var input = document.getElementById('imageInput').files[0];
    var reader = new FileReader();

    reader.onload = function() {
        preview.src = reader.result;
        preview.style.display = 'block';
    }

    if(input) {
        reader.readAsDataURL(input);
    } else {
        preview.src = '';
    }
}

document.getElementById('imageInput').addEventListener('change', previewImage);