from django.urls import path
from . import views

urlpatterns = [
    path("", views.homepage, name="main"),
    path("search", views.search, name="search"),
    path("board", views.board, name="board"),
    path("search_result", views.search_result, name="search_result"),
    path("mypage", views.mypage, name="mypage"),
    path("profile_edit", views.profile_edit, name="profile_edit"),
]
