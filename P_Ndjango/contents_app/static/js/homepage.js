var recipe_contents_container = document.getElementsByClassName("recipe_contents_container");
var recipe_content = document.getElementsByClassName("recipe_content");
var categories_contents_area = document.getElementsByClassName("categories_contents_area");


// Simple and tasty recipes
for (var i = 0; i < 3; i++ ){
    for (var j = 0; j < 3; j++){
        recipe_contents_container[i].appendChild(recipe_content[0])
    }
};

var categories_contents_area = document.getElementsByClassName
("categories_contents_area");
var categoryTitleElement = document.querySelectorAll(".category_title p");
var categories_content = `
    <div class="categories_content">
        <div class="category_img">

        </div>
        <div class="category_title">
            <p>쌀밥</p>
        </div>
    </div>
`;
var categories = ["밥", "베지테리언", "닭", "돼지", "소", "생선"];

for (var i = 0; i < 6; i++) {
    categories_contents_area[0].innerHTML += categories_content
}
var categoryTitleElement = document.querySelectorAll(".category_title p");
for (var i = 0; i < 6; i ++){
    categoryTitleElement[i].textContent = categories[i];

}



