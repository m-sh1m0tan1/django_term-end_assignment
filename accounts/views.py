from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.views import LoginView
from django.core.exceptions import PermissionDenied

from .forms import CustomUserCreationForm

# Create your views here.


class SignUpView(generic.CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("attendance:ModelListView")
    template_name = "accounts/signup.html"

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs


class CustomLoginView(LoginView):
    def get_success_url(self):
        # print('get_success_url')
        user = self.request.user
        if user.role == 1:
            # print('先生')
            return reverse_lazy("attendance:ModelListView")
        elif user.role == 2:
            return reverse_lazy("attendance:StudentAttendView")
        raise PermissionDenied("不正なユーザーです。")


class StudentSignupView(generic.CreateView):
    template_name = "accounts/signup_students.html"
