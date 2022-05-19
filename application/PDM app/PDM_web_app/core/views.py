from django.shortcuts import render,redirect
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.conf import settings
from django.db.models import Q
import json
import pandas as pd
import datetime
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
    date = datetime.datetime.now(datetime.timezone.utc)
    context = {}
    current_hour = date.hour
    current_date = date.date()
    print(current_date.day, current_hour, date)
    sensor_one = SensorOneData.objects.filter(Q(created_at__hour=current_hour-2), Q(created_at__day=current_date.day)).values('x_axis','y_axis', 'created_at')
    sensor_two = SensorTwoData.objects.filter(Q(created_at__hour=current_hour), Q(created_at=current_date)).values('x_axis','y_axis', 'created_at')
    context['sensor_one'] = list(sensor_one)
    context['sensor_two'] = list(sensor_two)
    return render(request, 'core/instantaneous_bearing_data.html', context)