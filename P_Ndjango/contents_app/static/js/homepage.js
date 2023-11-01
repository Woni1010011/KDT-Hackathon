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
        (function(i) { // 즉시 실행 함수를 추가
            var category_content = document.createElement('div');
            category_content.className = 'categories_content';

            var category_img = document.createElement('div');
            category_img.className = 'category_img';

            var img = document.createElement('img');
            img.src = imageUrls[i];
            img.alt = '';
            
            // 이미지를 클릭하면 새로운 URL로 리디렉션하는 이벤트 리스너를 추가합니다.
            img.addEventListener('click', function() {
                window.location.href = "http://127.0.0.1:8000/categories_result?q=" + categories[i];
            });

            category_img.appendChild(img);

            var category_title = document.createElement('div');
            category_title.className = 'category_title';

            var p = document.createElement('p');
            p.textContent = categories[i];

            category_title.appendChild(p);

            category_content.appendChild(category_img);
            category_content.appendChild(category_title);

            categories_contents_area.appendChild(category_content);
        })(i); // 즉시 실행 함수를 호출하고, 변수 i를 전달
    }
});

