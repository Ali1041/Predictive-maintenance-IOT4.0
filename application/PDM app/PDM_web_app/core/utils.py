import datetime
from .models import SensorOneData,SensorTwoData,FeaturesObtained
from django.db.models import Q
import numpy as np
from scipy.stats import skew, kurtosis
from scipy import signal
from scipy.fft import fft, fftfreq




def fetch_data(previous_pk, latest_pk):

    sensor_one = SensorOneData.objects.filter(Q(id__gte=previous_pk),Q(id__lte=latest_pk)).values('x_axis', 'y_axis',
                                                                                          'created_at').order_by('pk')
    sensor_two = SensorTwoData.objects.filter(Q(id__gte=previous_pk),Q(id__lte=latest_pk)).values(
        'x_axis', 'y_axis', 'created_at').order_by('pk')
    return sensor_one, sensor_two

def get_features( previous_pk, latest_pk):
    features = FeaturesObtained.objects.filter(Q(id__gte=previous_pk),
                                              Q(id__lte=latest_pk)).values(
        'mean',
        'std',
        'crest',
        'clearance',
        'kurtosis',
        'skewness',
        'impulse',
        'shape',
    )
    return features

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


def get_envelope(data):
    sos = signal.butter(5, [2000, 6000], 'bandpass', fs=20000, output='sos')

    filtered = signal.sosfilt(sos, data)
    y = signal.hilbert(filtered)

    # y = signal.hilbert(x)
    env = ((y.real) ** 2 + (y.imag) ** 2) ** 0.5
    N = 20480
    SAMPLE_RATE = 20000

    yf = fft(env)
    y_axis = abs(yf)[:int(len(data) / 2)]
    xf = fftfreq(N, 1 / SAMPLE_RATE)
    # x_val = [int(item) for index, item in enumerate(xf) if index != 0]
    y_val = [abs(item) for index, item in enumerate(y_axis) if index != 0]
    return y_val

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