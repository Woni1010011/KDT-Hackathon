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
    return render(request, 'registration/signup.html')