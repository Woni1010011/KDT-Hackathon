function goToEditPage() {
    window.location.href = "profile_edit.html";
}

document.getElementById("save-button").addEventListener("click", function () {
    window.location.href = "my_page.html";
});

function previewImage(event) {
    var input = event.target;
    var reader = new FileReader();

    reader.onload = function () {
        var img = document.getElementById('preview');
        img.src = reader.result;
    };

    reader.readAsDataURL(input.files[0]);
}