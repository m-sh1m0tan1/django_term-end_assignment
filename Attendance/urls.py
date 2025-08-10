from django.urls import path
from .views import *
urlpatterns = [
    path('home/', IndexView.as_view(), name="IndexView"),
    path('registration/', RegistrationView.as_view(), name='RegistrationView'),
]
