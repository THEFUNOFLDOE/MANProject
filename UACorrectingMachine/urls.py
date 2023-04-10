from django.urls import path
from .views import *


urlpatterns = [
    path('', index, name='home'),
    path('about', about, name='about'),
    path('check?<str:text>&<int:nn_numb_predicts>', render_check, name='render_check')
]
