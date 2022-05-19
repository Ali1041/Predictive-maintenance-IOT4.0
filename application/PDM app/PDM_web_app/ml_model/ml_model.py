import numpy as np
import pandas as pd
import scipy
import os
from typing import Optional, Union
import math
from scipy import special
from math import log, e
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score
from sklearn.model_selection import cross_val_score, GridSearchCV
import pickle
# Root Mean Squared Sum
def get_rms(data):
    value = np.sqrt((data ** 2).sum() / len(data))
    rms_list = value
    return rms_list


# Peak to peak calculation
def calculate_p2p(df):
    return df.max().abs() + df.min().abs()


# extract shannon entropy (cut signals to 500 bins) Shannon's Entropy is simply the "amount of information" in a variable
def get_entropy(signal, base=None):
    vc = signal.value_counts(normalize=True, sort=False)
    base = e if base is None else base
    return -(vc * np.log(vc) / np.log(base)).sum()


# extract clearence factor
def calculate_clearence(df):
    result = ((np.sqrt(df.abs())).sum() / len(df)) ** 2

    return result



directory_path = './1st_test'
dataframe = pd.DataFrame \
    (columns=['mean' ,'std' ,'skewness' ,'kurtosis' ,'rms' ,'max' ,'peak_to_peak', 'crest', 'clearence', 'shape', 'impulse'])
healthy = 0
for file in os.listdir(directory_path):
    file_data = pd.read_csv(os.path.join(directory_path, file) ,sep='\t')
    if file == '2003.11.22.09.16.56':
        healthy = 1
    concerned_data = file_data.iloc[: ,5:6]
    mean = np.array(concerned_data.abs().mean())[0]
    standard_deviation = np.array(concerned_data.std())[0]
    skewness = np.array(concerned_data.skew())[0]
    kurtosis = np.array(concerned_data.kurtosis())[0]
    rms = np.array(get_rms(concerned_data))[0]
    max_abs = np.array(concerned_data.abs().max())[0]
    peak_2_peak = calculate_p2p(concerned_data)[0]
    crest = max_abs /rms
    clearence = np.array(calculate_clearence(concerned_data))[0]
    shape = rms / mean
    impulse = max_abs / mean

    dataframe = dataframe.append({
        'mean' :mean,
        'std' :standard_deviation,
        'skewness' :skewness,
        'kurtosis' :kurtosis,
        'rms' :rms,
        'max' :max_abs,
        'peak_to_peak' :peak_2_peak,
        'crest' :crest,
        'clearence' :clearence,
        'shape' :shape,
        'impulse' :impulse
    } ,ignore_index=True)


df = dataframe.copy(deep=True)
df.drop('rms', inplace=True, axis=1)
df.drop('max', inplace=True, axis=1)
df.drop('peak_to_peak', inplace=True, axis=1)
features = ['mean','std','skewness','kurtosis', 'crest', 'clearence', 'shape', 'impulse']
df = df.iloc[250:]
for index,col in enumerate(df):
    mean_value = df[col].mean()
    std_value = df[col].std()
    first_col = f"{df[col].name}_upper_limit"
    second_col = f"{df[col].name}_lower_limit"
    df.insert(8+index, first_col, df[col] > mean_value + std_value, True)
    df.insert(9+index, second_col, df[col] < mean_value - std_value, True)

df= df.replace(False, 0)
for name in features:
    df[f'{name}_limit'] = df.loc[:,[f"{name}_upper_limit",f"{name}_lower_limit"]].sum(axis=1)
    df.drop([f"{name}_upper_limit",f"{name}_lower_limit"], inplace=True, axis=1)

df['healthy'] = df.iloc[:,8:].sum(axis=1)
df['healthy'] = np.where(df["healthy"]>4, 1, 0)

independant_var = df.iloc[:,:8]
dependant_var = df.iloc[:,-1:]

x_train, x_test, y_train, y_test= train_test_split(independant_var, dependant_var, test_size= 0.40, random_state=0)
st_x= StandardScaler()
x_train= st_x.fit_transform(x_train)
x_test= st_x.transform(x_test)

classifier= LogisticRegression(random_state=0, C=0.1)
classifier.fit(x_train, y_train)

y_pred = classifier.predict(x_test)
cm= confusion_matrix(y_test ,y_pred)
acc = accuracy_score(y_test, y_pred)
cross_val_score(classifier, y_test, y_pred, cv=5)

filename = 'ml_model/logistic.pkl'
pickle.dump(classifier, open(filename, 'wb'))