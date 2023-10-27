function goToEditPage() {
    window.location.href = "{% url 'profile_edit' %}";
}

function previewImage(event) {
    var input = event.target;
    var reader = new FileReader();

    reader.onload = function () {
        var img = document.getElementById('preview');
        img.src = reader.result;
    };

    reader.readAsDataURL(input.files[0]);
}

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