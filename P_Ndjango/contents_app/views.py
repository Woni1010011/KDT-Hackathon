from django.shortcuts import render, redirect

from django.http import JsonResponse
from google.cloud import vision
from google.cloud.vision_v1 import types
from django.contrib import messages
from .models import Recipes, Board
from account_app.models import User
from django.shortcuts import render, get_object_or_404
import re
import ast
from django.db.models import Q
from . import receipe_search


# Create your views here.
def homepage(request):
    recipes = Recipes.objects.all()
    recipe_images = recipes.values_list("recipe_img", flat=True)

    def extract_order(direction):
        # 순서 번호 추출
        order = int(direction.split(".")[0])
        return order

    sorted_recipe_images = []
    for img in recipe_images:
        sorted_recipe_images.append(img.split(" ")[1])

    thumbnail = sorted_recipe_images[-1]

    return render(request, "homepage.html", {"recipes": recipes, "thumbnail": thumbnail})


def search(request):
    return render(request, "search.html")


# 사용자 이름 가져오기
def get_user_name(request):
    user_id = request.session.get("user_id")

    if user_id:
        try:
            # user_id에 해당하는 사용자 조회
            user = User.objects.get(user_id=user_id)
            user_nick = user.user_nick
            user_name = user.user_name

            if user_nick:
                return user_nick
            else:
                # user_nick이 없을 경우 user_name 값을 반환
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


def board(request, filter):
    if filter == "ALL":
        posts = Board.objects.all().order_by("-post_no")
    elif filter == "recipe":
        posts = Board.objects.filter(board_no=1).order_by("-post_no")
    elif filter == "talk":
        posts = Board.objects.filter(board_no=2).order_by("-post_no")
    elif filter == "my":
        user_id = request.session.get("user_id")
        try:
            user = User.objects.get(user_id=user_id)
            user_nick = user.user_nick
            user_name = user.user_name

            # user_nick으로 게시물 필터링
            posts_nick = Board.objects.filter(user_nick=user_nick).order_by("-post_no")

            # user_name으로 게시물 필터링
            posts_name = Board.objects.filter(user_nick=user_name).order_by("-post_no")

            # 두 결과를 합칩니다.
            posts = posts_nick | posts_name
        except User.DoesNotExist:
            # 사용자를 찾을 수 없는 경우의 처리
            posts = []

    return render(request, "board.html", {"posts": posts, "filter": filter})


def search_result(request):
    query = request.GET.get("q")
    if query:
        results = Board.objects.filter(post_title__icontains=query)
    else:
        results = Board.objects.all()

    return render(request, "search_result.html", {"posts": results})


def mypage(request):
    return render(request, "my_page.html")


def profile_edit(request):
    return render(request, "profile_edit.html")


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
    # 레시피스 테이블 내용들을 불러옴
    recipe = Recipes.objects.get(pk=recipe_no)

    # ingredients 필드를 파싱
    ingredients_list = ast.literal_eval(recipe.ingredients)

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

    # 마지막 썸네일 이미지 제거
    sorted_recipe_images = sorted_recipe_images[:-1]

    # 사진이 없는 조리과정의 경우에 대한 처리를 위해 zip_longest를 사용
    # from itertools import zip_longest
    # directions_and_images = list(zip_longest(sorted_directions))

    # 결과를 post.html 템플릿에 전달
    return render(
        request,
        "recipe.html",
        {
            "recipe": recipe,
            "ingredients_list": ingredients_list,
            "directions": sorted_directions,
            "recipe_images": sorted_recipe_images,
            "thumbnail": thumbnail,
        },
    )  # 'recipe_images' : sorted_recipe_images


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


# post_view 함수 정의
def post_view(request, post_no):
    post = get_object_or_404(Board, post_no=post_no)
    # if "delete-button" in request.POST:
    #     post.delete()
    #     return redirect("board")

    post.post_hit += 1
    post.save()

    context = {
        "post": post,
    }

    return render(request, "post.html", context)
