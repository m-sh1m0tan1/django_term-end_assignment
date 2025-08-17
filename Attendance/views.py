from django.shortcuts import render
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import *
# Create your views here.

class ModelListView(LoginRequiredMixin, generic.ListView):
    # home/
    model = Subject
    context_object_name = 'Subject'
    template_name = 'attendance/home.html'

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['Period'] = Period.objects.all()
        context_data['Attend'] = Attend.objects.all()
        context_data['ReplacementInfo'] = ReplacementInfo.objects.all()
        return context_data
    

class SubjectCreateView(LoginRequiredMixin, generic.CreateView):
    # registration/
    model = Subject
    template_name = 'attendance/SubjectCreate.html'
    fields = '__all__'