// HTML 에서 사용할 ID 값 정의
const ingredientSearchLink = document.getElementById("ingredientSearchLink");
const imageSearchLink = document.getElementById("imageSearchLink");
const searchLink = document.getElementById("searchLink");

// page 이동없이 전환하는 코드
recipeSearchLink.addEventListener("click", function(event) {
    event.preventDefault();
});

// "search" 버튼을 눌렀을 때 "search.html" 페이지로 이동하는 함수
searchLink.addEventListener("click", function() {
    window.location.href = "{% url 'search' %}"; // "search.html" 페이지로 이동
});