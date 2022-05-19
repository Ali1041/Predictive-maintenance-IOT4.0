from django.shortcuts import render,redirect
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
# Create your views here.
@csrf_exempt
def get_pi_data(request):
    body_unicode = request.body.decode('utf-8')
    data_body = json.loads(body_unicode)
    print(data_body)
    return JsonResponse({"msg":'Processing starting!!!!'})


def home(request):
    return render(request, 'core/index.html')
