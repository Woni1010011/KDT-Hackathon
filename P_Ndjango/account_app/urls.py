from django.urls import path
from . import views

urlpatterns = [
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("social_login_view/", views.social_login_view, name="social_login"),
    path("signup/", views.signup_view, name="signup"),
    path("home/", views.home_page, name="homepage"),
    path("ndjango/", views.my_fridge, name="ndjango"),
    path('add_to_fridge/', views.add_to_fridge, name='add_to_fridge'),
    path('delete_to_fridge/<int:user_igrd_id>/', views.delete_to_fridge, name='delete_to_fridge'),
    path('ndjango/material/', views.ndjango_material, name='ndjango_material'),
    path('ndjango/img/', views.ndjango_img, name='ndjango_img')
]
