from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.db import IntegrityError

from accounts.mixins import ForTeachersMixin
from .models import *
from .forms import * # フォーム
from datetime import date

# Create your views here.

class ModelListView(LoginRequiredMixin, ForTeachersMixin, generic.ListView):
    # home/
    model = Subject
    context_object_name = 'Subject'
    template_name = 'attendance/home.html'

    def get_queryset(self):
        quaryset =  super().get_queryset()
        return quaryset.order_by('charge_teacher')

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['Attend'] = Attend.objects.all()
        context_data['ReplacementInfo'] = ReplacementInfo.objects.all()
        # 曜日×時限の二次元配列を作成（例：2時限分）
        timetable = []
        year = datetime.now().year
        month = datetime.now().month
        semester = 1
        year_expect = [1, 2, 3]
        semester_expect = [9, 10, 11, 12, 1, 2, 3]
        if month in year_expect:
            year -= 1
        if month in semester_expect:
            semester = 2
        print(year, month, semester)
        
        for period in range(1, 5):  
            row = []
            for day in range(1, 6): 
                subjects = Period.objects.filter(day_of_week=day, period=period, semester=semester, year=year)
                row.append(subjects)
            timetable.append(row)
        context_data['timetable'] = timetable
        return context_data
    
class PeriodSemester1View(LoginRequiredMixin, ForTeachersMixin, generic.ListView):
    year = datetime.now().year
    month = datetime.now().month
    semester = 1
    year_expect = [1, 2, 3]
    # semester_expect = [9, 10, 11, 12, 1, 2, 3]
    if month in year_expect:
        year -= 1
    # if month in semester_expect:
        # semester = 2
    print(year, month, semester)
    queryset = Period.objects.filter(year=year, semester=semester)
    template_name = 'attendance/PeriodList.html'
    context_object_name = 'Period'

class PeriodSemester2View(LoginRequiredMixin, ForTeachersMixin, generic.ListView):
    year = datetime.now().year
    month = datetime.now().month
    semester = 2
    year_expect = [1, 2, 3]
    # semester_expect = [9, 10, 11, 12, 1, 2, 3]
    if month in year_expect:
        year -= 1
    # if month in semester_expect:
        # semester = 2
    print(year, month, semester)
    queryset = Period.objects.filter(year=year, semester=semester)
    template_name = 'attendance/PeriodList.html'
    context_object_name = 'Period'

class SubjectCreateView(LoginRequiredMixin, ForTeachersMixin, generic.CreateView):
    # 
    model = Subject
    template_name = 'attendance/SubjectCreate.html'
    # fields = '__all__'
    form_class = SubjectCreateForm
    
    def form_invalid(self, form):
        # ユニーク制約違反のエラーを削除
        unique_error_keys = []
        for field, errors in form.errors.items():
            for error in errors:
                if 'unique' in error.lower() or '既に存在' in error:
                    unique_error_keys.append(field)
        for key in unique_error_keys:
            del form.errors[key]
        # 独自メッセージを表示
        messages.error(self.request, "同じ名前の教科が既に登録されています。")
        return super().form_invalid(form)
    
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
            return redirect(reverse_lazy('attendance:ModelListView'))
        
    def get_success_url(self):
        return self.object.get_absolute_url()
    
class PeriodCreateView(LoginRequiredMixin, ForTeachersMixin,  generic.CreateView):
    model = Period
    template_name = 'attendance/PeriodCreate.html'
    form_class = PeriodCreateForm
    
    def form_invalid(self, form):
        # ユニーク制約違反のエラーを削除
        unique_error_keys = []
        for field, errors in form.errors.items():
            for error in errors:
                if 'unique' in error.lower() or '既に存在' in error:
                    unique_error_keys.append(field)
        for key in unique_error_keys:
            del form.errors[key]
        # 独自メッセージを表示
        messages.error(self.request, "同じ時間割が既に登録されています。")
        return super().form_invalid(form)
    
    def form_valid(self, form):
        try:
            self.object = form.save()
        except Exception as e:
            print(e)
        day_of_week = ['月', '火', '水', '木', '金']
        continue_adding = form.cleaned_data.get('continue_adding')
        if continue_adding:
            messages.success(self.request, f'{self.object.subject}を{day_of_week[self.object.day_of_week - 1]}曜日{self.object.period}限目に設定しました。')

            return redirect(reverse_lazy('attendance:PeriodCreateView'))
        
        else:
            return redirect(reverse_lazy('attendance:ModelListView'))
        
    def get_absolute_url(self):
        return self.object.get_absolute_url()
    
class SubjectUpdateView(LoginRequiredMixin, ForTeachersMixin,  generic.UpdateView):
    model = Subject
    template_name = 'attendance/SubjectCreate.html'
    fields = '__all__'


class PeriodUpdateView(LoginRequiredMixin, ForTeachersMixin,  generic.UpdateView):
    model = Period
    template_name = 'attendance/PeriodCreate.html'
    fields = '__all__'

class SubjectDeleteView(LoginRequiredMixin, ForTeachersMixin,  generic.DeleteView):
    model = Subject
    template_name = 'attendance/SubjectDelete.html'
    success_url = reverse_lazy('attendance:ModelListView')
    
class PeriodDeleteView(LoginRequiredMixin, ForTeachersMixin,  generic.DeleteView):
    model = Period
    template_name = 'attendance/PeriodDelete.html'
    success_url = reverse_lazy('attendance:ModelListView')
    
class StudentAttendView(LoginRequiredMixin, generic.CreateView):
    template_name = 'attendance/Attend.html'
    model = Attend
    form_class = StudentAttendForm
    success_url = reverse_lazy('attendance:StudentAttendView')
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
    
    def form_valid(self, form):
        form.instance.student = self.request.user
        try:
            self.object = form.save()
        except IntegrityError:
            messages.error(self.request, 'すでに出席済です。')
            return self.form_invalid(form)
        except Exception as e:
            print(e)
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['AttendanceRecord'] = Attend.objects.filter(student=self.request.user.id, time__date=date.today())
        return context_data
    
class MyPageView(LoginRequiredMixin, ForTeachersMixin, generic.ListView):
    model = Attend
    template_name = 'attendance/Mypage.html'