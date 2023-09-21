# 냉Django 해방일지
## Git Convention
- **[Add] [serializers.py](http://serializers.py) 생성, styles.css 생성**
⇒ 새로운 파일 추가하는 경우

- **[Feat] (구체적인 경우) class Article 추가, def write_article 추가, view에 index.html 파일 연결, (포괄적인 경우) 글쓰기 기능 구현, 글 공유 기능 구현**
⇒ 파일 내 새로운 클래스나 함수 등 추가하는 경우, url 연결 혹은 새로운 기능 추가하는 경우

- **[Fix] url path 변경, [settings.py](http://settings.py) 내 DB 설정 변경, 로그인 오류 해결**
⇒ 오류 수정, 오타 수정 등등 오류 해결하는 경우

- **[Docs] 프로젝트 설명 내용 변경, 화면 캡쳐 추가**
⇒ README 파일이나 기타 문서 수정하는 경우

- **[Remove] test.html 삭제**
⇒ 불필요한 파일 삭제하는 경우