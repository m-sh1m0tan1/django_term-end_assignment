from django.urls import path
from .views import *

app_name = 'attendance'

urlpatterns = [
    path('home/', ModelListView.as_view(), name="ModelListView"),
    path('SubjectCreate/', SubjectCreateView.as_view(), name='SubjectCreateView'),
    path('PeriodCreate/', PeriodCreateView.as_view(), name='PeriodCreateView'),
    path('SubjectUpdate/<int:pk>/', SubjectUpdateView.as_view(), name="SubjectUpdateView"),
    path('PeriodUpdate/<int:pk>/', PeriodUpdateView.as_view(), name="PeriodUpdateView"),
    path('SubjectDelete/<int:pk>/', SubjectDeleteView.as_view(), name="SubjectDeleteView"),
    path('PeriodDelete/<int:pk>/', PeriodDeleteView.as_view(), name="PeriodDeleteView"),
]
