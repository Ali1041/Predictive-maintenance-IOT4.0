import datetime
from .models import SensorOneData,SensorTwoData,FeaturesObtained
from django.db.models import Q
import numpy as np
from scipy.stats import skew, kurtosis

def fetch_data():
    date = datetime.datetime.now(datetime.timezone.utc)
    current_hour = date.hour
    current_date = date.date()
    sensor_one = SensorOneData.objects.filter(Q(created_at__hour=18),
                                              Q(created_at__day=current_date.day)).values('x_axis', 'y_axis',
                                                                                          'created_at')
    sensor_two = SensorTwoData.objects.filter(Q(created_at__hour=current_hour), Q(created_at__day=current_date.day)).values(
        'x_axis', 'y_axis', 'created_at')
    return sensor_one, sensor_two

def get_features(sensor_name, axis):
    date = datetime.datetime.now(datetime.timezone.utc)
    current_hour = date.hour
    current_date = date.date()
    features = FeaturesObtained.objects.filter(Q(created_at__hour=18),
                                              Q(created_at__day=current_date.day), name__iexact=sensor_name, axis=axis).values(
        'mean',
        'std',
        'crest',
        'clearance',
        'kurtosis',
        'skewness',
        'impulse',
        'shape',
    )
    return features[0]

def get_fft(inp):
    fft_time = np.arange(0,1, 1/len(inp))
    dt = (fft_time[1]-fft_time[0])
    n = int(1/dt)
    fhat = abs(np.fft.fft(inp,n))/n
    freq = (1/(dt*n))* np.arange(n)
    L = np.arange(1, np.floor(n/2), dtype='int')

#     plt.xlim(freq[L[0]], f_lim)
#     plt.legend()

    return (freq[L], fhat[L])



def calculate_clearence(df):
    result = ((np.sqrt(abs(df))).sum() / len(df)) ** 2
    return result

def get_rms(data):
    value = np.sqrt((data ** 2).sum() / len(data))
    rms_list = value
    return rms_list

def make_features(array, name, axis):
    mean = abs(array).mean()
    standard_deviation = array.std()
    skewness = skew(array)
    kurtosis_val = kurtosis(array)
    rms = get_rms(array)
    max_abs = max(abs(array))
    crest = max_abs /rms
    clearence = calculate_clearence(array)
    shape = rms / mean
    impulse = max_abs / mean
    FeaturesObtained.objects.create(
        name=name,
        axis=axis,
        mean=mean,
        std=standard_deviation,
        skewness=skewness,
        kurtosis=kurtosis_val,
        crest=crest,
        clearance=clearence,
        shape=shape,
        impulse=impulse
    )