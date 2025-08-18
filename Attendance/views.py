from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages

from .models import *
from .forms import * # フォーム

# Create your views here.

class ModelListView(LoginRequiredMixin, generic.ListView):
    # home/
    model = Subject
    context_object_name = 'Subject'
    template_name = 'attendance/home.html'

    def get_queryset(self):
        quaryset =  super().get_queryset()
        return quaryset.order_by('charge_teacher')

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['Period'] = Period.objects.all()
        context_data['Attend'] = Attend.objects.all()
        context_data['ReplacementInfo'] = ReplacementInfo.objects.all()
        return context_data
    

class SubjectCreateView(LoginRequiredMixin, generic.CreateView):
    # 
    model = Subject
    template_name = 'attendance/SubjectCreate.html'
    # fields = '__all__'
    form_class = SubjectCreateForm
    
    def form_valid(self, form):
        self.object = form.save()
        
        # チェックボックスの値を取得
        continue_adding = form.cleaned_data.get('continue_adding')
        if continue_adding:
            # チェックボックスにチェックが入っていてユーザーが繰り返し入力を望む場合
            # 成功メッセージを設定
            messages.success(self.request, f'{self.object.subject_name}を登録しました。続けて登録可能です。')

            # 同じページにリダイレクト
            return redirect(reverse_lazy('attendance:SubjectCreateView'))
        
        else:
            return super().form_valid(form)
        
    def get_success_url(self):
        return self.object.get_absolute_url()
    
class PeriodCreateView(LoginRequiredMixin, generic.CreateView):
    model = Period
    template_name = 'attendance/PeriodCreate.html'
    form_class = PeriodCreateForm
    
    def form_valid(self, form):
        self.object = form.save()
        
        continue_adding = form.cleaned_data.get('continue_adding')
        if continue_adding:
            messages.success(self.request, f'{self.object.subject}を{self.object.day_of_week}曜日{self.object.period}限目に設定しました。')

            return redirect(reverse_lazy('attendance:PeriodCreateView'))
        
        else:
            return super().form_valid(form)
        
    def get_absolute_url(self):
        return self.object.get_absolute_url()