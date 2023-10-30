function goToEditPage() {
    window.location.href = "{% url 'profile_edit' %}";

}

document.getElementById('profile-picture').addEventListener('change', function () {
    var file = this.files[0];
    if (file) {
        var reader = new FileReader();
        reader.onload = function (event) {
            document.getElementById('preview').setAttribute('src', event.target.result);
        }
        reader.readAsDataURL(file);
    }
});


function previewImage(input) {
    var preview = document.getElementById('preview');
    var file = input.files[0];
    var reader = new FileReader();

    reader.onload = function () {
        preview.src = reader.result;
    }

    if (file) {
        reader.readAsDataURL(file);
    }
}

var profilePictureInput = document.getElementById('profile-picture');
profilePictureInput.addEventListener('change', function () {
    previewImage(this);
});

function showSection(my_fridge_section) {
    var sections = document.querySelectorAll('main section');
    sections.forEach(function (section) {
        section.style.display = 'none';
    });
    var selectedSection = document.getElementById(my_fridge_section);
    if (selectedSection) {
        selectedSection.style.display = 'block';
    }
}

function showSection(profile, user_details, bottom_buttons) {
    var sections = document.querySelectorAll('main section');
    sections.forEach(function (section) {
        section.style.display = 'none';
    });
    var selectedSection = document.getElementById(profile, user_details, bottom_buttons);
    if (selectedSection) {
        selectedSection.style.display = 'block';
    }
}

function showSection(alarm_list_section) {
    var sections = document.querySelectorAll('main section');
    sections.forEach(function (section) {
        section.style.display = 'none';
    });
    var selectedSection = document.getElementById(alarm_list_section);
    if (selectedSection) {
        selectedSection.style.display = 'block';
    }
}

function showSection(favorite_list_section) {
    var sections = document.querySelectorAll('main section');
    sections.forEach(function (section) {
        section.style.display = 'none';
    });
    var selectedSection = document.getElementById(favorite_list_section);
    if (selectedSection) {
        selectedSection.style.display = 'block';
    }
}

function showSection(current_watching_section) {
    var sections = document.querySelectorAll('main section');
    sections.forEach(function (section) {
        section.style.display = 'none';
    });
    var selectedSection = document.getElementById(current_watching_section);
    if (selectedSection) {
        selectedSection.style.display = 'block';
    }
}