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

// view all contents 클릭시 이동
const allCategoryButton = document.getElementById("view_all_category").addEventListener("click", function(){
    window.location.href = "{% url 'board.html' %}";
});

const recipes = [
    {
        title: "Big and Juicy Wagyu Beef",
        time: "30 minutes",
        category: "Beef",
    },
    {
        title: "Delicious Veggie Stir-Fry",
        time: "20 minutes",
        category: "Vegetarian",
    },
    {
        title: "Spicy Grilled Chicken",
        time: "45 minutes",
        category: "Poultry",
    },
];

// 레시피 미리보기를 생성하는 함수
function createRecipePreview(recipe) {
    const recipeContent = document.createElement("div");
    recipeContent.className = "recipe_content";

    recipeContent.innerHTML = `
        <div class="recipe_image">
            <!-- 이미지를 여기에 추가 -->
        </div>
        <div class="recipe_title">
            <span>${recipe.title}</span>
        </div>
        <div class="recipe_info">
            <span>Time: ${recipe.time}</span>
            <span>Category: ${recipe.category}</span>
        </div>
    `;

    return recipeContent;
}

// 레시피 미리보기를 생성하고 추가
const recipeContainer = document.getElementById("recipeContainer");

for (const recipe of recipes) {
    const recipePreview = createRecipePreview(recipe);
    recipeContainer.appendChild(recipePreview);
}