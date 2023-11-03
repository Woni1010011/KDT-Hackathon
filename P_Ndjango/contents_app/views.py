from django.shortcuts import render, redirect
from django.http import JsonResponse
from google.cloud import vision
from google.cloud.vision_v1 import types
from django.contrib import messages
from .models import Recipes, Board, Ingredients
from account_app.models import User
from django.shortcuts import render, get_object_or_404
import re
import ast
import random
from django.db.models import Q
from . import receipe_search
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from django.templatetags.static import static
from urllib.parse import unquote
from itertools import chain
from account_app.views import ndjango_matching




# Create your views here.
def homepage(request):
    user_recommends = ndjango_matching(request)
    recipes = Recipes.objects.order_by("?")[:9]
    recipe_images = [recipe.recipe_img for recipe in recipes]

    def urlString(queryset):
        list_url = queryset.split(",")
        match = re.search(r'https://[^\s}"]+', list_url[-1])
        if match:
            url = match.group()
            return url
        else:
            print("매칭된 URL이 없습니다.")

    thumbnails = []
    for i in range(9):
        thumbnails.append(urlString(recipe_images[i]))

    mylist = zip(recipes, thumbnails)
    context = {
        "user_recommends" : user_recommends,
        "mylist": mylist,
    }

    return render(request, "homepage.html", context)


def search(request):
    # Ingredients 테이블에서 모든 레코드의 개수 가져오기
    total_ingredients_count = Ingredients.objects.count()

    # 중복되지 않는 10개의 레코드를 무작위로 선택
    igrd = []
    while len(igrd) < 10:
        random_index = random.randint(1, total_ingredients_count)
        ingredient = Ingredients.objects.filter(pk=random_index).first()
        if ingredient and ingredient not in igrd:
            igrd.append(ingredient)

    recipes = Recipes.objects.order_by("?")[:4]
    recipe_images = [recipe.recipe_img for recipe in recipes]

    def urlString(queryset):
        list_url = queryset.split(",")
        match = re.search(r'https://[^\s}"]+', list_url[-1])
        if match:
            url = match.group()
            return url
        else:
            print("매칭된 URL이 없습니다.")

    thumbnails = []
    for i in range(4):
        thumbnails.append(urlString(recipe_images[i]))

    mylist = zip(recipes, thumbnails)
    context = {
        "igrd": igrd,
        "mylist": mylist,
    }

    # 템플릿 렌더링
    return render(request, "search.html", context)


# 사용자 이름 가져오기
def get_user_name(request):
    user_id = request.session.get("user_id")

    if user_id:
        try:
            # user_id에 해당하는 사용자 조회
            user = User.objects.get(user_id=user_id)
            user_name = user.user_name

            return user_name
        except User.DoesNotExist:
            # 사용자가 존재하지 않을 때
            return None
    else:
        return None


def material_search(request):
    if request.method == "POST":
        image = request.FILES["image"]  # FILES를 따로 한 이유가 있
        file_name = "./contents_app/static/img/" + image.name

        with open(file_name, "wb") as file:
            for chunk in image.chunks():
                file.write(chunk)

        content = image.read()
        image = types.Image(content=content)
        text = receipe_search.tempFunction(file_name)  # receipt_image to text

        return render(request, "material_search.html", {"text": text})

    return render(request, "material_search.html")


# 이미지 검색
from googletrans import Translator


def img_search(request):
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

            return render(request, "img_search.html", {"translated_objects": filtered_objects})
        else:
            messages.warning(request, "재료를 찾을 수 없습니다.")
            return render(request, "img_search.html")
    else:
        return render(request, "img_search.html")


from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def board(request, filter):
    # filter 값에 따라 게시글을 가져옵니다.
    if filter == "ALL":
        posts = Board.objects.all().order_by("-post_no")
    elif filter == "recipe":
        posts = Board.objects.filter(board_no=1).order_by("-post_no")
    elif filter == "talk":
        posts = Board.objects.filter(board_no=2).order_by("-post_no")
    elif filter == "my":
        user_id = request.session.get("user_id")
        if user_id:
            user = User.objects.filter(user_id=user_id).first()
            if user:
                posts = Board.objects.filter(user_nick=user.user_name).order_by("-post_no")
            else:
                posts = Board.objects.none()  # 사용자를 찾을 수 없는 경우 빈 쿼리셋
        else:
            posts = Board.objects.none()  # 로그인하지 않은 사용자 처리

    # 검색 로직 추가
    query = request.GET.get('query')
    if query:
        posts = posts.filter(post_content__icontains=query)

    # 한 페이지당 게시물 수를 정의합니다.
    paginator = Paginator(posts, 10)  # 페이지당 10개의 게시글

    # URL에서 페이지 번호를 가져옵니다.
    page = request.GET.get("page")
    try:
        items = paginator.page(page)
    except PageNotAnInteger:
        items = paginator.page(1)  # 페이지 번호가 정수가 아닐 경우 첫 페이지를 반환합니다.
    except EmptyPage:
        items = paginator.page(paginator.num_pages)  # 페이지 범위를 벗어날 경우 마지막 페이지를 반환합니다.

    # 페이징 처리된 각 게시물에 대해 썸네일 URL을 설정합니다.
    for post in items:
        post.thumbnail_url = extract_first_image(post.post_content) if post.post_content else None

    # 템플릿에 전달할 컨텍스트에 페이지 객체를 추가합니다.
    icon_photo = static('img/icon_photo.png')
    return render(
        request,
        "board.html",
        {"posts": items, "filter": filter, "icon_photo": icon_photo},  # icon_photo 변수를 추가합니다.
    )

def my_preprocessor(text):
    # "밥"이라는 단어를 별도로 처리
    text = text.replace('밥', ' 밥 ')
    return text


def extract_first_image(post_content):
    img_pattern = re.compile(r'<img [^>]*src="([^"]+)')
    match = img_pattern.search(post_content)
    return match.group(1) if match else None

def search_result(request):    
    query = request.GET.get("q", "")
    query = unquote(query)
    if not query:
        return redirect("search")

    # 레시피, 게시글 데이터 가져오기
    recipes = Recipes.objects.all()
    boards = Board.objects.all()

    # "간편요리" 키워드가 입력되었을 때 20분 이내의 레시피만 필터링
    if query == "간편요리":
        # cook_time 필드의 문자열을 분 단위로 변환하는 함수
        def parse_cook_time(cook_time):
            if '분' in cook_time:
                return int(cook_time.split('분')[0])
            return 0

        # cook_time 필드를 분 단위로 변환해서 필터링
        recipes = [recipe for recipe in recipes if parse_cook_time(recipe.cook_time) <= 20]

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

    # 랜덤한 게시물 4개 선택
    random_recipes = Recipes.objects.order_by('?')[:4]
    
    random_recipes_with_thumbnail = []
    for recipe in random_recipes:
        recipe_images = ast.literal_eval(recipe.recipe_img)
        
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
        random_recipes_with_thumbnail.append((recipe, thumbnail))

    # 인기있는 게시물 3개 선택
    popular_boards = Board.objects.order_by('-post_hit')[:3]
    
    popular_boards_with_thumbnail = []
    for board in popular_boards:
        thumbnail = extract_first_image(board.post_content)
        popular_boards_with_thumbnail.append((board, thumbnail))
    
    # 렌더링할 컨텍스트에 인기있는 게시물 추가
    context = {
        'items': items,
        'query': query,
        'random_recipes_with_thumbnail': random_recipes_with_thumbnail,
        'icon_photo': static('img/icon_photo.png'),
        'popular_boards_with_thumbnail': popular_boards_with_thumbnail,
    }

    return render(request, 'search_result.html', context)

from datetime import datetime

def categories_result(request):
    query = request.GET.get("q")

    # For Recipes
    if query:
        recipe_results = Recipes.objects.filter(Q(recipe_title__icontains=query) | Q(ingredients__icontains=query))
    else:
        recipe_results = Recipes.objects.all()
    # For Boards
    if query:
        board_results = Board.objects.filter(Q(post_content__icontains=query) | Q(board_no=1))
    else:
        board_results = Board.objects.all()

    # Combine the two querysets without sorting
    combined_results_list = list(chain(recipe_results, board_results))
    # Pagination for combined results
    paginator = Paginator(combined_results_list, 15)  # Show 15 items per page.
    page = request.GET.get('page')
    items_on_page = paginator.get_page(page)

    return render(request, "categories_result.html", {
        "items": items_on_page,
        "query": query
    })
    
def mypage(request):
    if request.session.get("user_id"):
        user_id = request.session["user_id"]

        try:
            user = User.objects.get(user_id=user_id)
            template = "my_page.html"  # 템플릿 경로 수정
            context = {"user": user}
            return render(request, template, context)
        except User.DoesNotExist:
            # 사용자가 존재하지 않을 경우에 대한 처리
            return redirect("login")

    return redirect("login")


def profile_edit(request):
    # user_id = request.session["user_id"]
    if request.method == "POST":
        new_nickname = request.POST.get("new_nickname")
        new_address = request.POST.get("new_address")

        # User 테이블에서 현재 사용자를 가져오는 코드
        user = User.objects.get(user_id=request.session.get("user_id"))

        # 닉네임 필드 업데이트
        user.user_nick = new_nickname
        user.user_address = new_address

        # 이미지 업데이트 처리
        if "new_image" in request.FILES:
            user.image = request.FILES["new_image"]

        user.save()

        # 성공적으로 업데이트되었음을 나타내는 응답 전송
        return redirect("mypage")

    return render(request, "my_page.html")


def recipe_list(request):
    recipes = Recipes.objects.all()  # 모든 레시피를 가져옵니다.
    return render(request, "recipes/recipe_list.html", {"recipes": recipes})


# def get_ingredients(ingredients_text):
#     while True:
#         new_text = re.sub(r'\b0+(\d)', r'\1', ingredients_text)
#         if new_text == ingredients_text:  # 더 이상 변화가 없으면 반복을 종료
#             break
#         ingredients_text = new_text

#     # 문자열을 리스트로 변환
#     raw_ingredients = ast.literal_eval(ingredients_text)

#     # 재료와 양 분리
#     ingredients = []
#     for item in raw_ingredients:
#         # " " 기준으로 나누기
#         split_item = item.split(' ')
#         ingredient = split_item[0]
#         amount = ' '.join(split_item[1:])
#         ingredients.append({"ingredient": ingredient, "amount": amount})

#     return ingredients


# recipe_view 함수 정의
def recipe_view(request, recipe_no):
    # 레시피 테이블 내용을 불러옴
    recipe = Recipes.objects.get(pk=recipe_no)

    def parse_ingredients(ingredients_str):
        try:
            # 시도해서 파이썬 리터럴로 파싱
            ingredients = ast.literal_eval(ingredients_str)
            if isinstance(ingredients, set):
                return list(ingredients)

        except (SyntaxError, ValueError):
            pass

        # 처리할 수 없는 경우, 문자열을 쉼표로 분할하여 리스트로 반환
        ingredients = [
            item.strip("''").strip('"') for item in ingredients_str.strip("{}").split(",")
        ]
        ingredients = [ingredient.strip() for ingredient in ingredients]
        return ingredients

    # 필드를 파싱
    ingredients_list = parse_ingredients(recipe.ingredients)
    directions = ast.literal_eval(recipe.direction)
    recipe_images = ast.literal_eval(recipe.recipe_img)

    def extract_order(direction):
        # 순서 번호 추출
        order = int(direction.split(".")[0])
        return order

    # 정렬된 directions 리스트 생성
    sorted_directions = sorted(directions, key=extract_order)
    recipe_images = sorted(recipe_images, key=extract_order)

    sorted_recipe_images = []
    for img in recipe_images:
        sorted_recipe_images.append(img.split(" ")[1])

    thumbnail = sorted_recipe_images[-1]
    sorted_recipe_images = sorted_recipe_images[:-1]

    template = "recipe.html"
    recipelist = zip(sorted_recipe_images, sorted_directions)

    popular_boards = Board.objects.order_by('-post_hit')[:3]

    popular_boards_with_thumbnail = []
    for board in popular_boards:
        thumbnails = extract_first_image(board.post_content)
        popular_boards_with_thumbnail.append((board, thumbnails))
    
    random_recipes = Recipes.objects.order_by('?')[:4]
    random_recipes_with_thumbnail = []
    for temp_recipe in random_recipes:
        recipe_images = ast.literal_eval(temp_recipe.recipe_img)
        
        def extract_order(direction):
            # 순서 번호 추출
            order = int(direction.split(".")[0])
            return order
        
        # 정렬된 directions 리스트 생성
        sorted_recipe_images = sorted(recipe_images, key=extract_order)
        
        sorted_imgs = []
        for img in sorted_recipe_images:
            sorted_imgs.append(img.split(" ")[1])
        
        temp_thumbnail = sorted_imgs[-1] if sorted_imgs else None
        random_recipes_with_thumbnail.append((temp_recipe, temp_thumbnail))


    context = {
        "recipe": recipe,
        "ingredients_list": ingredients_list,
        "recipelist" : recipelist,
        "thumbnail": thumbnail,
        "popular_boards_with_thumbnail" : popular_boards_with_thumbnail,
        'icon_photo': static('img/icon_photo.png'),
        'random_recipes_with_thumbnail': random_recipes_with_thumbnail,
    }

    return render(request, template, context)


from .forms import PostForm


def write_post(request):
    user_name = get_user_name(request)

    if request.method == "POST":
        form = PostForm(request.POST)

        if form.is_valid():
            post = form.save(commit=False)
            post.user_nick = user_name
            post.save()
            post_no = post.post_no
            return redirect("post", post_no=post_no)
    else:
        form = PostForm()

    return render(request, "write_post.html", {"write_form": form})


def edit_post(request, post_no=None):
    user_name = get_user_name(request)

    if post_no is not None:
        post = get_object_or_404(Board, post_no=post_no)
        if post.user_nick != user_name:
            # 글 작성자가 아닌 경우에는 수정할 수 없도록 처리
            return redirect("post", post_no=post_no)

    if request.method == "POST":
        form = PostForm(request.POST, instance=post)

        if form.is_valid():
            post = form.save(commit=False)
            post.user_nick = user_name
            post.save()
            # post_no = post.post_no
            return redirect("post", post_no=post.post_no)

        elif "delete" in request.POST:  # "delete" 버튼이 클릭된 경우 글을 삭제합니다.
            post.delete()
            return redirect("main")
    else:
        form = PostForm(instance=post)

    template = "edit_post.html"
    context = {
        "write_form": form,
        "post": post,
        "edit_mode": post_no is not None,
    }

    return render(request, template, context)


# post_view 함수 정의
def post_view(request, post_no):
    user_name = get_user_name(request)
    user_recommends = ndjango_matching(request)
    post = get_object_or_404(Board, post_no=post_no)

    post.post_hit += 1
    post.save()

    context = {
        "post": post,
        "user_name": user_name,
        "user_recommends": user_recommends,
    }

    return render(request, "post.html", context)
