from django.shortcuts import render

# Create your views here.
def homepage(request):
    return render(request, 'homepage.html')

def search(reqeust):
    return render(reqeust, 'search.html')