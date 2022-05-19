from django.urls import path
from core import views

app_name = 'core'

urlpatterns = [
    path('', views.get_pi_data, name='pi_data'),
    path('home/', views.home, name='home')
]