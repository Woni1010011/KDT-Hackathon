from django.contrib import auth
from django.shortcuts import render, redirect
from .models import User
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

# Create your views here.

@csrf_exempt
def login_view(request):
    template = 'registration/login.html'

    if request.method == 'POST':
        inputId = request.POST.get('id', '')  # 사용자가 입력한 ID
        inputPassword = request.POST.get('password', '')  # 사용자가 입력한 비밀번호

        try:
            user = User.objects.get(user_id=inputId)  # 입력한 ID로 사용자 조회
            if user.user_password == inputPassword:
                # 로그인에 성공하면 세션에 사용자 ID 저장
                request.session['user_id'] = user.user_id
                return redirect('main')  # 로그인 성공 시 리디렉션할 페이지로 이동
            else:
                context = {
                    "result": "비밀번호가 틀렸습니다"
                }
        except User.DoesNotExist:
            context = {
                "result": "존재하지 않는 id입니다"
            }
    else:
        context = {}  # GET 요청일 경우, 빈 컨텍스트 전달

    return render(request, template, context)

def social_login_view(request):
    return render(request, 'registration/login.html')

def signup_view(request):
    return render(request, 'registration/signup.html')

def home_page(request) :
    return render(request, 'home_page.html')