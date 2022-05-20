from django.shortcuts import render,redirect
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.conf import settings
import json
import pandas as pd
import numpy as np
import datetime
from .models import SensorOneData, SensorTwoData
from .utils import fetch_data, make_features, get_features, get_fft

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
    sensor_one_x_array = np.array(sensor_one_x)
    make_features(sensor_one_x_array, 'S1B1', 'x')

    sensor_one_y_array = np.array(sensor_one_y)
    make_features(sensor_one_y_array, 'S1B2', 'x')

    sensor_two_x_array = np.array(sensor_two_x)
    make_features(sensor_two_x_array, 'S2B1', 'x')

    sensor_two_y_array = np.array(sensor_two_y)
    make_features(sensor_two_y_array, 'S2B2', 'x')
    SensorOneData.objects.bulk_create(sensor_one)
    SensorTwoData.objects.bulk_create((sensor_two))
    return render(request, 'core/index.html')

def home(request):
    return render(request, 'core/index.html')


def instantaneous_bearing_data(request):
    context = {}
    sensor_one,sensor_two = fetch_data()
    context['sensor_one'] = list(sensor_one)
    context['sensor_two'] = list(sensor_two)
    return render(request, 'core/instantaneous_bearing_data.html', context)


def bearing_history(request):
    context = {}
    sensor_one,sensor_two = fetch_data()
    features = get_features('S1B1', 'x')
    s1_x_axis_data = list(sensor_one.values_list('x_axis'))
    # s1_y_axis_data = list(sensor_one.values_list('y_axis'))
    # s2_x_axis_data = list(sensor_one.values_list('x_axis'))
    # s2_y_axis_data = list(sensor_one.values_list('y_axis'))
    x_axis, y_axis = get_fft(s1_x_axis_data)
    context['sensor_one'] = list(sensor_one)
    context['sensor_two'] = list(sensor_two)
    context['feature'] = features
    context['x_axis'] = list(x_axis)
    context['y_axis'] = list(y_axis)
    return render(request, 'core/bearing_history.html', context)

def time_features(request):
    context = {}
    sensor_one,sensor_two = fetch_data()
    context['sensor_one'] = list(sensor_one)
    context['sensor_two'] = list(sensor_two)
    return render(request, 'core/time_features.html', context)


def main_dashboard(request):
    context = {}
    sensor_one,sensor_two = fetch_data()
    context['sensor_one'] = list(sensor_one)
    context['sensor_two'] = list(sensor_two)
    return render(request, 'core/main_dashboard.html', context)