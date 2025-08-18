from django.urls import path
from .views import *

app_name = 'attendance'

urlpatterns = [
    path('home/', ModelListView.as_view(), name="ModelListView"),
    path('SubjectCreate/', SubjectCreateView.as_view(), name='SubjectCreateView'),
    path('PeriodCreate/', PeriodCreateView.as_view(), name='PeriodCreateView'),
]
