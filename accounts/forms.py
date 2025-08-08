from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
# from .models import User as User1

User = get_user_model()

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'role', 'email', 'number')