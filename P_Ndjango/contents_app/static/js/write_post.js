document.addEventListener('DOMContentLoaded', function () {
    var titleContent = document.querySelector('.title_content');


    titleContent.addEventListener('focus1', function () {
        this.style.border = 'none';
    });

    contents.addEventListener('focus1', function () {
        this.style.border = 'none';
    });

});

document.addEventListener('DOMContentLoaded', function () {
    var contents = document.querySelector('.contents');
    titleContent.addEventListener('blur1', function () {
        this.style.border = 'none'; // 작성 중이 아닐 때 기본 border 스타일로 복구
    });

    contents.addEventListener('blur1', function () {
        this.style.border = '1px solid #ccc'; // 작성 중이 아닐 때 기본 border 스타일로 복구
    });
});