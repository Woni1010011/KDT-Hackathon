from django.shortcuts import render
from django.http import JsonResponse
from google.cloud import vision
from google.cloud.vision_v1 import types

# Create your views here.
def homepage(request):
    return render(request, 'homepage.html')

def search(request):
    return render(request, 'search.html')

def material_search(request):
    return render(request, 'material_search.html')

def img_search(request):
    if request.method == 'POST' and request.FILES['image']:
        image = request.FILES['image']
        client = vision.ImageAnnotatorClient()

        content = image.read()
        image = types.Image(content=content)
        response = client.object_localization(image=image)
        objects = response.localized_object_annotations

        if objects:
            detected_objects = [obj.name for obj in objects]
            return JsonResponse({'detected_objects': detected_objects})
        else:
            return JsonResponse({'error': 'No objects detected in the image'})
    else:
        return render(request, 'img_search.html')    

def board(request):
    return render(request, 'board.html')

def search_result(request):
    return render(request, 'search_result.html')

def mypage(request):
    return render(request, 'my_page.html')

def profile_edit(request):
    return render(request, 'profile_edit.html')

def post(request) :
    return render(request, 'post.html')