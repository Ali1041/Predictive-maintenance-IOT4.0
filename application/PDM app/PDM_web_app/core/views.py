from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.conf import settings
import json
import pandas as pd
import numpy as np
from scipy.fft import fft, fftfreq
import os
from .models import SensorOneData, SensorTwoData, FeaturesObtained
from .utils import fetch_data, make_features, get_features, get_fft, get_envelope
import pickle
from django.db.models import Q

# Create your views here.


@csrf_exempt
def get_pi_data(request):
    body_unicode = request.body.decode('utf-8')
    data_body = json.loads(body_unicode)
    print(data_body)
    return JsonResponse({"msg": 'Processing starting!!!!'})


def load_data(request):
    # 2004.02.12.10.32.39
    # 2004.02.19.06.22.39
    url = settings.STATIC_ROOT + '/2nd_test/2004.02.19.06.22.39'

    directory_path = settings.STATIC_ROOT+'/bleh'
    for file in os.listdir(directory_path):
        file_data = pd.read_csv(os.path.join(directory_path, file), sep='\t')
        file_data.columns = ['B1x', 'B1y', 'B2x', 'B2y']
        B1x = list(file_data['B1x'])
        B1y = list(file_data['B1y'])
        B2x = list(file_data['B2x'])
        B2y = list(file_data['B2y'])
        sensor_one = []
        sensor_two = []
        for index, item in enumerate(B1x):
            sensor_one.append(SensorOneData(x_axis=item, y_axis=B1y[index]))
            sensor_two.append(SensorTwoData(x_axis=B2x[index], y_axis=B2y[index]))

        request.session['previous_pk'] = SensorOneData.objects.latest(
            'pk').pk if SensorOneData.objects.all().exists() else 1

        SensorOneData.objects.bulk_create(sensor_one)
        SensorTwoData.objects.bulk_create(sensor_two)
        request.session['current_pk'] = SensorOneData.objects.latest('pk').pk

        request.session['feature_previous_pk'] = FeaturesObtained.objects.latest(
            'pk').pk if FeaturesObtained.objects.all().exists() else 1

        B1x_array = np.array(B1x)
        make_features(B1x_array, 'S1B1', 'x')

        B1y_array = np.array(B1y)
        make_features(B1y_array, 'S1B2', 'y')

        B2x_array = np.array(B2x)
        make_features(B2x_array, 'S2B1', 'x')

        B2y_array = np.array(B2y)
        make_features(B2y_array, 'S2B2', 'y')
        request.session['features_current_pk'] = FeaturesObtained.objects.latest('pk').pk

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
    context = {}
    latest_pk = request.session['current_pk']
    previous_pk = request.session['previous_pk']
    feature_latest_pk = request.session['features_current_pk']
    feature_previous_pk = request.session['feature_previous_pk']
    sensor_one = sensor_two = ''
    if 'q' in request.GET.keys():
        parts = latest_pk / 4
        print(parts)
        mapping = {'14:00':[0, parts], '15:00':[parts,parts*2],'16:00':[parts*2,parts*3],'17:00':[parts*3,parts*4]}
        print(request.GET, mapping[f'{request.GET["q"]}'])
        points = mapping[f'{request.GET["q"]}']
        sensor_one = SensorOneData.objects.filter(Q(pk__gte=points[0]), Q(pk__lte=points[1])).values('x_axis', 'y_axis',
                                                                                          'created_at').order_by('pk')
        sensor_two = SensorTwoData.objects.filter(Q(pk__gte=points[0]), Q(pk__lte=points[1])).values('x_axis', 'y_axis',
                                                                                          'created_at').order_by('pk')
    else:
        sensor_one, sensor_two = fetch_data(previous_pk, latest_pk)

        features = get_features(feature_previous_pk, feature_latest_pk)
    context['sensor_one'] = list(sensor_one)
    context['sensor_two'] = list(sensor_two)
    context['features'] = features
    context['is_files'] = True
    return render(request, 'core/bearing_history.html', context)


def time_features(request):
    context = {}
    features_one_x = FeaturesObtained.objects.filter(axis='x', name='S1B1').values().order_by('pk')
    features_one_y = FeaturesObtained.objects.filter(axis='y', name='S1B2').values().order_by('pk')
    features_two_x = FeaturesObtained.objects.filter(axis='x', name='S2B1').values().order_by('pk')
    features_two_y = FeaturesObtained.objects.filter(axis='y', name='S2B2').values().order_by('pk')
    context['features_one_x'] = list(features_one_x)
    context['features_one_y'] = list(features_one_y)
    context['features_two_x'] = list(features_two_x)
    context['features_two_y'] = list(features_two_y)
    return render(request, 'core/time_features.html', context)


def main_dashboard(request):
    context = {}
    prediction_val = {
        0:'Healthy',
        1:'Faulty',
    }
    latest_pk = request.session['current_pk']
    previous_pk = request.session['previous_pk']
    sensor_one, sensor_two = fetch_data(previous_pk, latest_pk)
    feature = FeaturesObtained.objects.latest('pk')
    feature_list = [feature.mean, feature.std, feature.skewness, feature.kurtosis,feature.crest,feature.clearance,feature.shape,feature.impulse]
    loaded_model = pickle.load(
        open("C:\\Users\\DELL\\Documents\\All projects\FYP\\application\\PDM app\\PDM_web_app\\core\\logistic.pkl", 'rb'))
    prediction = loaded_model.predict([feature_list])
    context['sensor_one'] = list(sensor_one)
    context['sensor_two'] = list(sensor_two)
    context['result'] = prediction_val[prediction[0]]
    return render(request, 'core/main_dashboard.html', context)
