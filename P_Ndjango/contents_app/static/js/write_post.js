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

document.getElementById('publish-btn').addEventListener('click', function () {
    // 폼 데이터 수집
    var title = document.getElementById('post_title').value; // 제목 필드 ID를 사용
    var content = $('.summernote').summernote('code'); // Summernote 내용 가져오기

    // 내용이 비었나 확인
    if (title.trim() === '' || content.trim() === '') {
        alert('제목과 내용을 모두 입력해주세요.'); // 에러 메시지
        return; // 함수 종료
    }

    // 폼 데이터를 FormData 객체로 만들기
    var formData = new FormData();
    formData.append('csrfmiddlewaretoken', '{{ csrf_token }}');
    formData.append('post_title', title);
    formData.append('post_content', content);

    // AJAX를 사용하여 데이터 전송
    $.ajax({
        url: '{% url ' / write_post / ' %}', // 뷰의 URL 패턴을 사용
        type: 'post',
        data: formData,
        processData: false,
        contentType: false,
        success: function (data) {
            alert('게시물이 발행되었습니다.');
            // 성공 시 처리
        },
        error: function (xhr, status, error) {
            // 에러 처리
        }
    });
});