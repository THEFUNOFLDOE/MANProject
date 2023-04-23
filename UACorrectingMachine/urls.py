from django.urls import path
from .views import *


urlpatterns = [
    path('', index, name='home'),
    path('about', about, name='about'),
    path('instruction', instruction, name='instruction'),
    path('example-<int:id>', render_example, name='render_example'),
]
