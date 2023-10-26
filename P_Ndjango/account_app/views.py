from django.shortcuts import render, redirect
from .models import User
from django.views.decorators.csrf import csrf_exempt


# Create your views here.

@csrf_exempt
def login_view(request):
    template = 'registration/login.html'
    if request.session.get('user_id'):
        # 이미 로그인된 사용자는 메인 페이지로 리디렉션
        return redirect('main')
    else:
        
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

def logout_view(request) : 
    if request.session.get('user_id'):
        del request.session['user_id']
    
    # 로그아웃 후 리디렉션할 페이지로 이동 (예: 로그인 페이지)
    return redirect('main')