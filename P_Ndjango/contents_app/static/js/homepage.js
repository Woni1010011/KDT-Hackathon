var recipe_contents_container = document.getElementsByClassName("recipe_contents_container");
var recipe_content = document.getElementsByClassName("recipe_content");
var categories_contents_area = document.getElementsByClassName("categories_contents_area");


// Simple and tasty recipes
for (var i = 0; i < 3; i++ ){
    for (var j = 0; j < 3; j++){
        recipe_contents_container[i].appendChild(recipe_content[0])
    }
};

document.addEventListener("DOMContentLoaded", function() {
    var categories_contents_area = document.getElementsByClassName("categories_contents_area")[0];

    for (var i = 0; i < imageUrls.length; i++) {
        var category_content = document.createElement('div');
        category_content.className = 'categories_content';

        var category_img = document.createElement('div');
        category_img.className = 'category_img';

        var img = document.createElement('img');
        img.src = imageUrls[i];
        img.alt = '';

        category_img.appendChild(img);

        var category_title = document.createElement('div');
        category_title.className = 'category_title';

        var p = document.createElement('p');
        p.textContent = categories[i];

        category_title.appendChild(p);

        category_content.appendChild(category_img);
        category_content.appendChild(category_title);

        categories_contents_area.appendChild(category_content);
    }
});


