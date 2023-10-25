from django.contrib import auth
from django.shortcuts import render, redirect
# Create your views here.


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = auth.authenticate(request, username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('login')
        else:
            return render(request, 'registration/login.html'), {'error':'ID와 비밀번호를 확인해 주세요.'}
    return render(request, 'registration/login.html')

def social_login_view(request):
    return render(request, 'registration/login.html')

def signup_view(request):
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        password = request.POST.get('password')
        password_check = request.POST.get('password_check')
        user_name = request.POST.get('user_name')
        user_email = request.POST.get('user_email')
        user_nick = request.POST.get('user_nick')
        user_phone = request.POST.get('user_phone')
        user_address = request.POST.get('user_address')
        
        if password == password_check:
            user = User.objects.create_user(
                user_id=user_id,
                password=password,
                user_name=user_name,
                user_email=user_email,
                user_nick=user_nick,
                user_phone=user_phone,
                user_address=user_address,
            )
            login(request, user)
            return redirect('homepage')
        else:
            messages.error(request, '비밀번호가 일치하지 않습니다.')
    return render(request, 'registration/signup.html')

def home_page(request) :
    return render(request, 'home_page.html')