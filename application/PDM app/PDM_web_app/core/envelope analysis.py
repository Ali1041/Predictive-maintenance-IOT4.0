#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy import signal, stats
plt.rcParams['figure.figsize'] = [24, 6]
plt.rcParams.update({'font.size': 10})


# In[2]:


def get_fft(time, inp):
    dt = (time[1]-time[0])
    n = int(1/dt)
    fhat = abs(np.fft.fft(inp,n))/n
    freq = (1/(dt*n))* np.arange(n)
    L = np.arange(1, np.floor(n/2), dtype='int')

#     plt.xlim(freq[L[0]], f_lim)
#     plt.legend()

    return (freq[L], fhat[L])


# In[3]:


dataset = pd.read_csv('C:/Users/Hp/Documents/FYP/data/2nd_test/2nd_test/2004.02.17.16.02.39', sep='\t')
dataset.columns = ['B1','B2','B3','B4']
# dataset.columns = ['B1x', 'B1y', 'B2x', 'B2y', 'B3x', 'B3y', 'B4x', 'B4y', ]
ax = dataset.iloc[:,0:1].plot(figsize = (24,6), title= "Bearing Vibration" , legend = True)
ax.set(xlabel="cycle(n)", ylabel="vibration/acceleration(g)")
plt.show()


# In[4]:


x = dataset['B1'].to_numpy()
x = np.append(x, 0)
len(x)


# In[5]:


t = np.arange(0,1.024, 1/20000)
len(t)


# In[6]:


sos = signal.butter(5, [2000 ,6000], 'bandpass', fs=20000, output='sos')

filtered = signal.sosfilt(sos, x)
print(stats.kurtosis(filtered))
plt.plot(filtered)


# In[7]:


get_fft(t,x)


# In[8]:


from scipy.fft import fft, fftfreq

y = signal.hilbert(filtered)

# y = signal.hilbert(x)
env = ((y.real)**2 + (y.imag)**2)**0.5
plt.plot(env)

# Number of samples in normalized_tone


# In[9]:


N = 20480
SAMPLE_RATE = 20000

yf = fft(env)
xf = fftfreq(N, 1 / SAMPLE_RATE)

plt.plot(xf, np.abs(yf))
plt.show()


# In[47]:


out = xf[np.where(abs(yf)>120)]
out


# In[48]:


out = out/33
out


# In[18]:


def round(n):
    if abs(n) - abs(int(n)) <0.5:
        return int(n)
    else:
        if n>0: return int(n) + 1
        else: return int(n) - 1


# In[49]:


res = []
for i in out:
    if i - round(i) < 0.05 and i - round(i) > -0.05:
        res.append(round(i))
res


# In[50]:


len(res)


# In[250]:


sos = signal.butter(5, [2000 ,6000], 'bandpass', fs=20000, output='sos')


# In[70]:


import os
new_directory_path = 'C:/Users/Hp/Documents/FYP/data/2nd_test/2nd_test/bleh2'
bpfo = []
bpfi = []
bpr = []

for n, file in enumerate(os.listdir(new_directory_path)):
    print(n)
    file_data = pd.read_csv(os.path.join(new_directory_path, file),sep='\t')
    concerned_data = file_data.iloc[:,0:1]
    b1 = np.array(concerned_data)
    b1 =  [i[0] for i in b1]
    b1.append(0)
    b1 = np.array(b1)
    
    filtered = signal.sosfilt(sos, b1)
    
    y = signal.hilbert(filtered)
    env = ((y.real)**2 + (y.imag)**2)**0.5
    
    yf = fft(env)
    xf = fftfreq(N, 1 / SAMPLE_RATE)
    out = xf[np.where(abs(yf)>50)]/230.5
    
    out = xf[np.where(abs(yf)>100)]/33.203125
    count = 0
    for i in out:
        if i - round(i) < 0.05 and i - round(i) > -0.05:
            count = count +1
    bpfi.append(count)

    out = xf[np.where(abs(yf)>100)]/230.46875
    count = 0
    for i in out:
        if i - round(i) < 0.05 and i - round(i) > -0.05:
            count = count +1
    bpfo.append(count)

    out = xf[np.where(abs(yf)>100)]/14.5
    count = 0
    for i in out:
        if i - round(i) < 0.05 and i - round(i) > -0.05:
            count = count +1
    bpr.append(count)
    


# In[71]:


plt.plot(bpfo)


# In[72]:


plt.plot(bpfi)


# In[73]:


plt.plot(bpr)


# In[66]:


import os
new_directory_path = 'C:/Users/Hp/Documents/FYP/data/1st_test/1st_test/bleh2'
bpfo = []
bpfi = []
bpr = []

for n, file in enumerate(os.listdir(new_directory_path)):
    print(n)
    file_data = pd.read_csv(os.path.join(new_directory_path, file),sep='\t')
    concerned_data = file_data.iloc[:,4:5]
    b1 = np.array(concerned_data)
    b1 =  [i[0] for i in b1]
    b1.append(0)
    b1 = np.array(b1)
    
    filtered = signal.sosfilt(sos, b1)
    
    y = signal.hilbert(filtered)
    env = ((y.real)**2 + (y.imag)**2)**0.5
    
    yf = fft(env)
    xf = fftfreq(N, 1 / SAMPLE_RATE)
    
    out = xf[np.where(abs(yf)>100)]/33.203125
    count = 0
    for i in out:
        if i - round(i) < 0.05 and i - round(i) > -0.05:
            count = count +1
    bpfi.append(count)

    out = xf[np.where(abs(yf)>100)]/230.46875
    count = 0
    for i in out:
        if i - round(i) < 0.05 and i - round(i) > -0.05:
            count = count +1
    bpfo.append(count)

    out = xf[np.where(abs(yf)>100)]/14.5
    count = 0
    for i in out:
        if i - round(i) < 0.05 and i - round(i) > -0.05:
            count = count +1
    bpr.append(count)

    


# In[67]:


plt.plot(bpfo)


# In[68]:


plt.plot(bpfi)


# In[69]:


plt.plot(bpr)


# In[62]:


xf[np.where(abs(yf)>300)]


# In[74]:


import os
new_directory_path = 'C:/Users/Hp/Documents/FYP/data/1st_test/1st_test/bleh2'
bpfo = []
bpfi = []
bpr = []

for n, file in enumerate(os.listdir(new_directory_path)):
    print(n)
    file_data = pd.read_csv(os.path.join(new_directory_path, file),sep='\t')
    concerned_data = file_data.iloc[:,6:7]
    b1 = np.array(concerned_data)
    b1 =  [i[0] for i in b1]
    b1.append(0)
    b1 = np.array(b1)
    
    filtered = signal.sosfilt(sos, b1)
    
    y = signal.hilbert(filtered)
    env = ((y.real)**2 + (y.imag)**2)**0.5
    
    yf = fft(env)
    xf = fftfreq(N, 1 / SAMPLE_RATE)
    
    out = xf[np.where(abs(yf)>100)]/33.203125
    count = 0
    for i in out:
        if i - round(i) < 0.05 and i - round(i) > -0.05:
            count = count +1
    bpfi.append(count)

    out = xf[np.where(abs(yf)>100)]/230.46875
    count = 0
    for i in out:
        if i - round(i) < 0.05 and i - round(i) > -0.05:
            count = count +1
    bpfo.append(count)

    out = xf[np.where(abs(yf)>100)]/14.5
    count = 0
    for i in out:
        if i - round(i) < 0.05 and i - round(i) > -0.05:
            count = count +1
    bpr.append(count)


# In[75]:


plt.plot(bpfo)


# In[76]:


plt.plot(bpfi)


# In[77]:


plt.plot(bpr)


# In[294]:


out = xf[np.where(abs(yf)>100)]/14.5


# In[295]:


res = []
for i in out:
    if i - round(i) < 0.1 and i - round(i) > -0.1:
        res.append(round(i))
len(res)


# In[64]:


out


# In[65]:


y = out/13.46982759
y


# In[ ]:




