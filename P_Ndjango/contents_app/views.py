from django.shortcuts import render

# Create your views here.
def homepage(request):
    return render(request, 'homepage.html')

def search(reqeust):
    return render(reqeust, 'search.html')

def material_search(reqeust):
    return render(reqeust, 'material_search.html')

def img_search(reqeust):
    return render(reqeust, 'img_search.html')

def board(reqeust):
    return render(reqeust, 'board.html')

def search_result(reqeust):
    return render(reqeust, 'search_result.html')

def mypage(request):
    return render(request, 'my_page.html')

def profile_edit(request):
    return render(request, 'profile_edit.html')