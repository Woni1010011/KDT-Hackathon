from django.shortcuts import render, redirect, get_object_or_404
from account_app.models import User, UserIgrd
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def login_view(request):
    template = "registration/login.html"
    if request.session.get("user_id"):
        # 이미 로그인된 사용자는 메인 페이지로 리디렉션
        return redirect("main")
    else:
        if request.method == "POST":
            inputId = request.POST.get("id", "")  # 사용자가 입력한 ID
            inputPassword = request.POST.get("password", "")  # 사용자가 입력한 비밀번호

            try:
                user = User.objects.get(user_id=inputId)  # 입력한 ID로 사용자 조회
                if user.user_password == inputPassword:
                    # 로그인에 성공하면 세션에 사용자 ID 저장
                    request.session["user_id"] = user.user_id
                    return redirect("main")  # 로그인 성공 시 리디렉션할 페이지로 이동
                else:
                    context = {"result": "비밀번호가 틀렸습니다"}
            except User.DoesNotExist:
                context = {"result": "존재하지 않는 id입니다"}
        else:
            context = {}  # GET 요청일 경우, 빈 컨텍스트 전달

        return render(request, template, context)


def social_login_view(request):
    return render(request, "registration/login.html")


@csrf_exempt
def signup_view(request):
    if request.method == "POST":
        user_id = request.POST["user_id"]
        user_password = request.POST["user_password"]
        password_check = request.POST["password_check"]
        user_name = request.POST["user_name"]
        user_email = request.POST["user_email"]
        user_nick = request.POST["user_nick"]
        user_phone = request.POST["user_phone"]
        user_address = request.POST["user_address"]

        if user_password == password_check:
            user = User.objects.create(
                user_id=user_id,
                user_password=user_password,
                user_name=user_name,
                user_email=user_email,
                user_nick=user_nick,
                user_phone=user_phone,
                user_address=user_address,
            )
            context = {"result": "가입이 완료되었습니다. 로그인해주세요."}
            return redirect("main")
        else:
            context = {"result": "비밀번호가 일치하지 않습니다."}
            return render(request, context)

    return render(request, "registration/signup.html")


def home_page(request):
    return render(request, "home_page.html")


def logout_view(request):
    if request.session.get("user_id"):
        del request.session["user_id"]

    # 로그아웃 후 리디렉션할 페이지로 이동
    return redirect("main")


def my_fridge(request):
    user_id = request.session.get("user_id")
    user_recommends = ndjango_matching(request)
    
    if user_id:
        # UserIgrd 테이블에서 세션에 있는 user_id와 같은 user_id를 갖는 정보를 가져옵니다.
        user_igrds = UserIgrd.objects.filter(user_id=user_id)
    else:
        user_igrds = ["내 냉장고가 비었습니다."]

    context = {
        "user_igrds": user_igrds,
        'user_recommends': user_recommends,
    }

    return render(request, "my_ndjango.html", context)

import re
def add_to_fridge(request):
    if request.method == "POST":
        user_id = request.session["user_id"]
        igrd_name = request.POST.get("igrd_name")
        user_igrd_date = request.POST.get("user_igrd_date")

        igrd_names = re.sub(r'\s+', '', igrd_name).split(',')

        for name in igrd_names:
            if name:
                user_igrd = UserIgrd.objects.create(
                    user_id=user_id, igrd_name=name, user_igrd_date=user_igrd_date
                )

        return redirect("ndjango")
    else:
        return render(request, "my_ndjango.html")
    

def delete_to_fridge(request, user_igrd_id):
    user_id = request.session["user_id"]
    user_igrd = UserIgrd.objects.get(id=user_igrd_id,user_id=user_id)
    user_igrd.delete()
    return redirect('ndjango')

from contents_app import receipe_search
from google.cloud.vision_v1 import types
def ndjango_material(request):
    if request.method == "POST":
        image = request.FILES["image"]  # FILES를 따로 한 이유가 있
        file_name = "./contents_app/static/img/" + image.name

        with open(file_name, "wb") as file:
            for chunk in image.chunks():
                file.write(chunk)

        content = image.read()
        image = types.Image(content=content)
        text = receipe_search.tempFunction(file_name)  # receipt_image to text

        return render(request, "my_ndjango.html", {"text": text})

    return render(request, "my_ndjango.html")

from googletrans import Translator
from google.cloud import vision
from django.contrib import messages
def ndjango_img(request):
    if request.method == "POST" and request.FILES["image"]:
        image = request.FILES["image"]
        client = vision.ImageAnnotatorClient()

        content = image.read()
        image = types.Image(content=content)
        # 이미지 객체를 텍스트로 변환
        response = client.object_localization(image=image)
        objects = response.localized_object_annotations

        if objects:
            detected_objects = [obj.name for obj in objects]
            unique_detected_objects = list(set(detected_objects))

            # 구글 번역 API 한국어로 번역 일일 사용량 제한있음
            translator = Translator()
            translated_objects = [
                translator.translate(obj, src="en", dest="ko").text
                for obj in unique_detected_objects
            ]

            # '음식' 및 '패키지 상품' 필터링
            filtered_objects = [
                obj for obj in translated_objects if obj not in ["음식", "패키지 상품", "채소"]
            ]
            return render(request, "my_ndjango.html", {"translated_objects": filtered_objects})
        else:
            messages.warning(request, "재료를 찾을 수 없습니다.")
            return render(request, "my_ndjango.html")
    else:
        return render(request, "my_ndjango.html")
    

from contents_app.models import Recipes, Board
from urllib.parse import unquote
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import ast
from django.templatetags.static import static

def extract_first_image(post_content):
    img_pattern = re.compile(r'<img [^>]*src="([^"]+)')
    match = img_pattern.search(post_content)
    return match.group(1) if match else None

def my_preprocessor(text):
    # "밥"이라는 단어를 별도로 처리
    text = text.replace('밥', ' 밥 ')
    return text

def ndjango_matching(request):
    user_id = request.session.get("user_id")
    user_igrds = UserIgrd.objects.filter(user_id=user_id)
    if user_igrds:
        # UserIgrd 테이블에서 user_id와 일치하는 데이터 가져오기
        unique_igrd_names = user_igrds.values('igrd_name').distinct()  # 중복 제거
        unique_igrd_names_list = [entry['igrd_name'] for entry in unique_igrd_names]  # 문자열변환
        unique_igrd_names_str = ', '.join(unique_igrd_names_list)

        query = unquote(unique_igrd_names_str)
        if not query:
            return redirect("ndjango")

        # 레시피, 게시글 데이터 가져오기
        recipes = Recipes.objects.all()
        boards = Board.objects.all()

        # 레시피 + 게시글 내용 리스트화
        contents_list = []

        contents_list = [
            (recipe.recipe_title, recipe.ingredients) for recipe in recipes
        ] + [
            (board.post_title, board.post_content) for board in boards
        ]

        # contents_list의 각 원소를 문자열로 변환합니다.
        contents_str_list = [
            ' '.join(map(str, content)) for content in contents_list
        ]
    
        # TfidfVectorizer를 사용하여 재료를 벡터로 변환합니다.  
        vectorizer = TfidfVectorizer(min_df=0.1, max_df=0.9, analyzer='char', preprocessor=my_preprocessor)
        tfidf_matrix = vectorizer.fit_transform(contents_str_list)
        # 사용자의 검색 쿼리를 벡터로 변환합니다.
        query_vec = vectorizer.transform([query])

        # 코사인 유사도를 계산합니다.
        cosine_similarities = cosine_similarity(query_vec, tfidf_matrix).flatten()

        # 코사인 유사도에 따라 레시피를 정렬합니다.
        all_data = list(recipes) + list(boards)
        similar_data = sorted(zip(cosine_similarities, all_data), key=lambda x: x[0], reverse=True)

        # 리스트로 변환
        similar_data = list(similar_data)

        # 상위 5개의 결과를 가져옵니다.
        top_data = [data for _, data in similar_data[:5]]

        items = []
        for data in top_data:
            if isinstance(data, Recipes):
                recipe_images = ast.literal_eval(data.recipe_img)

                def extract_order(direction):
                    # 순서 번호 추출
                    order = int(direction.split(".")[0])
                    return order

                # 정렬된 directions 리스트 생성
                sorted_recipe_images = sorted(recipe_images, key=extract_order)

                sorted_imgs = []
                for img in sorted_recipe_images:
                    sorted_imgs.append(img.split(" ")[1])

                thumbnail = sorted_imgs[-1] if sorted_imgs else None
                item = {
                    "thumbnail": thumbnail,
                    "title": data.recipe_title,
                    "url_name": "recipe",
                    "pk": data.recipe_no,
                }
                items.append(item)
            elif isinstance(data, Board):
                thumbnail = extract_first_image(data.post_content)
                item = {
                    'thumbnail': thumbnail,
                    'title': data.post_title,
                    'url_name': 'post',
                    'pk': data.post_no,
                }
                items.append(item)

        return items