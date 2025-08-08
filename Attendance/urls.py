from django.urls import path
from .views import IndexView
urlpatterns = [
    path('test/', IndexView.as_view(), name="Indexview"),
    
]
