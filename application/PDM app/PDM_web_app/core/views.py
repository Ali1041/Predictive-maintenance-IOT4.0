from django.shortcuts import render,redirect
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.conf import settings
import json
import pandas as pd

from .models import SensorOneData, SensorTwoData
# Create your views here.
@csrf_exempt
def get_pi_data(request):
    body_unicode = request.body.decode('utf-8')
    data_body = json.loads(body_unicode)
    print(data_body)
    return JsonResponse({"msg":'Processing starting!!!!'})

def load_data(request):
    # 2004.02.12.10.32.39
    url = settings.STATIC_ROOT+'/2nd_test/2004.02.12.10.32.39'
    dataset = pd.read_csv(url, sep='\t')
    dataset.columns = ['B1x', 'B1y', 'B2x', 'B2y']
    sensor_one_x = list(dataset['B1x'])
    sensor_one_y = list(dataset['B1y'])
    sensor_two_x = list(dataset['B2x'])
    sensor_two_y = list(dataset['B2y'])
    sensor_one = []
    sensor_two = []
    for index,item in enumerate(sensor_one_x):
        sensor_one.append(SensorOneData(x_axis=item, y_axis=sensor_one_y[index]))
        sensor_two.append(SensorTwoData(x_axis=sensor_two_x[index], y_axis=sensor_two_y[index]))

    SensorOneData.objects.bulk_create(sensor_one)
    SensorTwoData.objects.bulk_create((sensor_two))
    return render(request, 'core/index.html')

def home(request):
    return render(request, 'core/index.html')


def instantaneous_bearing_data(request):
    return render(request, 'core/instantaneous_bearing_data.html')