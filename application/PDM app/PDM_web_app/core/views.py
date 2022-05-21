from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.conf import settings
import json
import pandas as pd
import numpy as np
from scipy.fft import fft, fftfreq
import datetime
from scipy import signal

from .models import SensorOneData, SensorTwoData, FeaturesObtained
from .utils import fetch_data, make_features, get_features, get_fft, get_envelope


# Create your views here.


@csrf_exempt
def get_pi_data(request):
    body_unicode = request.body.decode('utf-8')
    data_body = json.loads(body_unicode)
    print(data_body)
    return JsonResponse({"msg": 'Processing starting!!!!'})


def load_data(request):
    # 2004.02.12.10.32.39
    url = settings.STATIC_ROOT + '/2nd_test/2004.02.12.10.32.39'

    dataset = pd.read_csv(url, sep='\t')
    dataset.columns = ['B1x', 'B1y', 'B2x', 'B2y']
    sensor_one_x = list(dataset['B1x'])
    sensor_one_y = list(dataset['B1y'])
    sensor_two_x = list(dataset['B2x'])
    sensor_two_y = list(dataset['B2y'])
    sensor_one = []
    sensor_two = []
    for index, item in enumerate(sensor_one_x):
        sensor_one.append(SensorOneData(x_axis=item, y_axis=sensor_one_y[index]))
        sensor_two.append(SensorTwoData(x_axis=sensor_two_x[index], y_axis=sensor_two_y[index]))

    request.session['feature_previous_pk'] = FeaturesObtained.objects.latest('pk').pk if FeaturesObtained.objects.all().exists() else 1

    sensor_one_x_array = np.array(sensor_one_x)
    make_features(sensor_one_x_array, 'S1B1', 'x')

    sensor_one_y_array = np.array(sensor_one_y)
    make_features(sensor_one_y_array, 'S1B2', 'y')

    sensor_two_x_array = np.array(sensor_two_x)
    make_features(sensor_two_x_array, 'S2B1', 'x')

    sensor_two_y_array = np.array(sensor_two_y)
    make_features(sensor_two_y_array, 'S2B2', 'y')
    request.session['features_current_pk'] = FeaturesObtained.objects.latest('pk').pk

    request.session['previous_pk'] = SensorOneData.objects.latest('pk').pk if SensorOneData.objects.all().exists() else 1
    SensorOneData.objects.bulk_create(sensor_one)
    SensorTwoData.objects.bulk_create(sensor_two)
    request.session['current_pk'] = SensorOneData.objects.latest('pk').pk
    return render(request, 'core/index.html')


def home(request):
    return render(request, 'core/index.html')


def instantaneous_bearing_data(request):
    context = {}
    latest_pk = request.session['current_pk']
    previous_pk = request.session['previous_pk']
    sensor_one, sensor_two = fetch_data(previous_pk, latest_pk)
    context['sensor_one'] = list(sensor_one)
    context['sensor_two'] = list(sensor_two)
    return render(request, 'core/instantaneous_bearing_data.html', context)


def fft_api(request):
    latest_pk = request.session['current_pk']
    previous_pk = request.session['previous_pk']
    sensor_one, sensor_two = fetch_data(previous_pk, latest_pk)
    s1_x_axis_data = list(sensor_one.values_list('x_axis'))
    s1_y_axis_data = list(sensor_one.values_list('y_axis'))
    s2_x_axis_data = list(sensor_one.values_list('x_axis'))
    s2_y_axis_data = list(sensor_one.values_list('y_axis'))

    slice_int = int(len(s1_x_axis_data)/2)

    fft_1_x = fft(s1_x_axis_data)
    y_1_x_val = [float(item) for item in abs(fft_1_x)[:slice_int]]

    fft_1_y = fft(s1_y_axis_data)
    y_1_y_val = [float(item) for item in abs(fft_1_y)[:slice_int]]

    fft_2_x = fft(s2_x_axis_data)
    y_2_x_val = [float(item) for item in abs(fft_2_x)[:slice_int]]

    fft_2_y = fft(s2_y_axis_data)
    y_2_y_val = [float(item) for item in abs(fft_2_y)[:slice_int]]

    return JsonResponse({'y_1_x_val': y_1_x_val,'y_1_y_val':y_1_y_val,'y_2_x_val':y_2_x_val,'y_2_y_val':y_2_y_val})


def envelope_spectrum(request):
    latest_pk = request.session['current_pk']
    previous_pk = request.session['previous_pk']
    sensor_one, sensor_two = fetch_data(previous_pk, latest_pk)
    s1_x_axis_data = list(sensor_one.values_list('x_axis'))
    s1_y_axis_data = list(sensor_one.values_list('y_axis'))
    s2_x_axis_data = list(sensor_one.values_list('x_axis'))
    s2_y_axis_data = list(sensor_one.values_list('y_axis'))

    s1_x_axis_data = [float(item[0]) for item in s1_x_axis_data]
    s1_y_axis_data = [float(item[0]) for item in s1_y_axis_data]
    s2_x_axis_data = [float(item[0]) for item in s2_x_axis_data]
    s2_y_axis_data = [float(item[0]) for item in s2_y_axis_data]

    y_one_x = get_envelope(s1_x_axis_data)
    y_one_y = get_envelope(s1_y_axis_data)
    y_two_x = get_envelope(s2_x_axis_data)
    y_two_y = get_envelope(s2_y_axis_data)
    return JsonResponse({'y_one_x':y_one_x, 'y_one_y':y_one_y,'y_two_x':y_two_x,'y_two_y':y_two_y})


def bearing_history(request):
    if request.method == 'POST':
        pass
    context = {}
    latest_pk = request.session['current_pk']
    previous_pk = request.session['previous_pk']
    sensor_one, sensor_two = fetch_data(previous_pk, latest_pk)
    feature_latest_pk = request.session['features_current_pk']
    feature_previous_pk = request.session['feature_previous_pk']
    features = get_features(feature_previous_pk, feature_latest_pk)
    context['sensor_one'] = list(sensor_one)
    context['sensor_two'] = list(sensor_two)
    context['features'] = features
    return render(request, 'core/bearing_history.html', context)


def time_features(request):
    context = {}
    latest_pk = request.session['current_pk']
    previous_pk = request.session['previous_pk']
    sensor_one, sensor_two = fetch_data(previous_pk, latest_pk)
    context['sensor_one'] = list(sensor_one)
    context['sensor_two'] = list(sensor_two)
    return render(request, 'core/time_features.html', context)


def main_dashboard(request):
    context = {}
    latest_pk = request.session['current_pk']
    previous_pk = request.session['previous_pk']
    sensor_one, sensor_two = fetch_data(previous_pk, latest_pk)
    context['sensor_one'] = list(sensor_one)
    context['sensor_two'] = list(sensor_two)
    return render(request, 'core/main_dashboard.html', context)
