from django.urls import path
from core import views

app_name = 'core'

urlpatterns = [
    path('', views.main_dashboard, name='main-dashboard'),
    path('home/', views.home, name='home'),
    path('load-data/', views.load_data, name='load-data'),
    path('instant-bearing-data/', views.instantaneous_bearing_data, name='instant-bearing-data'),
    path('bearing-history', views.bearing_history, name='bearing-history'),
    path('time-features', views.time_features, name='time-features'),
    path('fft-api/', views.fft_api, name="fft-api"),
    path('envelope-api/',views.envelope_spectrum, name='envelope-spectrum'),
    path('post-data/', views.get_pi_data, name='pi_data'),
]