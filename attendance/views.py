from django.shortcuts import render
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
from urllib.parse import urlparse

# Create your views here.

class ModelListView(LoginRequiredMixin, ForTeachersMixin, generic.ListView):
    # home/
    model = Subject
    context_object_name = 'Subject'
    template_name = 'attendance/home.html'

    def get_queryset(self):
        quaryset =  super().get_queryset()
        return quaryset.order_by('charge_teacher', 'subject_name')

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
    template_name = 'attendance/PeriodList.html'
    context_object_name = 'timetable'
    
    def get_queryset(self):
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
        # queryset = Period.objects.filter(year=year, semester=semester)
        queryset = []
        for period in range(1, 5):  
            row = []
            for day in range(1, 6): 
                subjects = Period.objects.filter(day_of_week=day, period=period, semester=semester, year=year)
                row.append(subjects)
            queryset.append(row)
        return queryset

class PeriodSemester2View(LoginRequiredMixin, ForTeachersMixin, generic.ListView):
    template_name = 'attendance/PeriodList.html'
    context_object_name = 'timetable'

    def get_queryset(self):
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
        queryset = []
        for period in range(1, 5):  
            row = []
            for day in range(1, 6): 
                subjects = Period.objects.filter(day_of_week=day, period=period, semester=semester, year=year)
                row.append(subjects)
            queryset.append(row)
        return queryset

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
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        referer = self.request.META.get('HTTP_REFERER')
        if referer:
            parsed = urlparse(referer)
            if parsed.netloc == self.request.get_host() and parsed.path != self.request.path:
                if parsed.query:
                    context['back_url'] = parsed.path + '?' + parsed.query
                else:
                    context['back_url'] = parsed.path
            else:
                context['back_url'] = reverse_lazy('attendance:ModelListView')
        else:
            context['back_url'] = reverse_lazy('attendance:ModelListView')
        return context
    
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
        # 共通情報
        year = form.cleaned_data['year']
        semester = form.cleaned_data['semester']
        day_of_week = form.cleaned_data['day_of_week']
        period_num = form.cleaned_data['period']
        subjects = form.cleaned_data['subject']  # 複数選択

        created = []
        for subject in subjects:
            # 重複チェック
            if not Period.objects.filter(
                year=year,
                semester=semester,
                day_of_week=day_of_week,
                period=period_num,
                subject=subject
            ).exists():
                Period.objects.create(
                    year=year,
                    semester=semester,
                    day_of_week=day_of_week,
                    period=period_num,
                    subject=subject
                )
                created.append(subject.subject_name)
        if created:
            messages.success(self.request, f"{', '.join(created)} を登録しました。")
            # print(list(messages.get_messages(self.request)))
        else:
            messages.warning(self.request, "すべての教科が既に登録済みです。")

        # 続けて登録
        if form.cleaned_data.get('continue_adding'):
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
    # fields = '__all__'
    form_class = PeriodUpdateForm
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['Period'] = self.object
        referer = self.request.META.get('HTTP_REFERER')
        if referer:
            parsed = urlparse(referer)
            if parsed.netloc == self.request.get_host():
                if parsed.query:
                    context['back_url'] = parsed.path + '?' + parsed.query
                else:
                    context['back_url'] = parsed.path
            else:
                context['back_url'] = reverse_lazy('attendance:ModelListView')
        else:
            context['back_url'] = reverse_lazy('attendance:ModelListView')
        return context
    
    def get_success_url(self):
        # 更新前のsemesterをセッションなどで保持していない場合は、更新後の値しか参照できません
        # どうしても「更新前」の値で分岐したい場合は、form_validで一時的にself.old_semesterをセット
        semester = getattr(self, 'old_semester', self.object.semester)
        if semester == 1:
            return reverse_lazy('attendance:PeriodSemester1View')
        elif semester == 2:
            return reverse_lazy('attendance:PeriodSemester2View')
        else:
            return reverse_lazy('attendance:ModelListView')
    
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
        # 更新前のsemesterを一時保存
        self.old_semester = self.object.semester
        print(self.old_semester)
        return super().form_valid(form)

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
        # context_data['AttendanceRecord'] = Attend.objects.filter(student=self.request.user.id, time__date=date(2025, 8, 22))
        return context_data
    
class MyPageView(LoginRequiredMixin, ForTeachersMixin, generic.ListView):
    model = Attend
    template_name = 'attendance/Mypage.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        subjects = Subject.objects.filter(charge_teacher=user)
        # subject_attends = []
        # for subject in subjects:
        #     periods = Period.objects.filter(subject=subject)
        #     attends = Attend.objects.filter(period__in=periods).order_by('student__number')
        #     subject_attends.append({
        #         'subject': subject,
        #         'attends': attends,
        #     })
        # context['subject_attends'] = subject_attends
        context['subjects'] = subjects
        return context
    
class ReplacementView(LoginRequiredMixin, ForTeachersMixin, generic.CreateView):
    template_name = 'attendance/Replacement.html'
    model = ReplacementInfo
    form_class = ReplacementForm
    
    def get_initial(self):
        initial = super().get_initial()
        period_id = self.kwargs.get('pk')
        if period_id:
            initial['original_period'] = period_id
        return initial
    
    def get_form(self, form_class = None):
        form = super().get_form(form_class)
        subject_id = self.kwargs.get('pk')
        if subject_id:
            period = Period.objects.filter(subject_id=subject_id).first()
            if period:
                form.fields['original_period'].queryset = Period.objects.filter(id=period.id)
                form.fields['original_period'].empty_label = None
                # form.fields['original_period'].disabled = True
                form.instance.original_period = period
                form.initial['original_period'] = period
            
        return form
    
    def form_valid(self, form):
        subject_id = self.kwargs.get('pk')
        period = Period.objects.filter(subject_id=subject_id).first()
        cancel_date = form.cleaned_data['cancel_date']
        replacement_date = form.cleaned_data['replacement_date']

        if period and form.cleaned_data['original_period'] != period:
            messages.error(self.request, '不正な値が送信されました。')
            return self.form_invalid(form)
        if form.cleaned_data['cancel_date'] > form.cleaned_data['replacement_date']:
            messages.error(self.request, '無効な時間設定です。')
            return self.form_invalid(form)

        # cancel_dateの情報
        cancel_weekday = cancel_date.weekday() + 1
        cancel_year = cancel_date.year
        cancel_month = cancel_date.month
        cancel_semester = 1
        if cancel_month in [9, 10, 11, 12, 1, 2, 3]:
            cancel_semester = 2

        # replacement_dateの情報
        replacement_weekday = replacement_date.weekday() + 1
        replacement_year = replacement_date.year
        replacement_month = replacement_date.month
        replacement_semester = 1
        if replacement_month in [9, 10, 11, 12, 1, 2, 3]:
            replacement_semester = 2

        print('subject_id:', subject_id)
        print('cancel_weekday:', cancel_weekday)
        print('period_num:', period.period)
        print('cancel_year:', cancel_year)
        print('cancel_semester:', cancel_semester)
        # print('DB Period:', list(Period.objects.values()))
        
        if period:
            # cancel_dateに同じ授業が存在するか
            exists_cancel = Period.objects.filter(
                subject_id=subject_id,
                day_of_week=cancel_weekday,
                period=period.period,
                year=cancel_year,
                semester=cancel_semester
            ).exists()
            if not exists_cancel:
                messages.error(self.request, '休講元の日付として設定されたその日に該当の授業はありません。')
                return self.form_invalid(form)

            # cancel_dateに同じ授業が重複していないか
            same_cancel = Period.objects.filter(
                subject_id=subject_id,
                day_of_week=cancel_weekday,
                period=period.period,
                year=cancel_year,
                semester=cancel_semester
            ).count() > 1
            if same_cancel:
                messages.error(self.request, '休講元の日付・時間帯にすでに同じ授業が存在します。')
                return self.form_invalid(form)

            # replacement_dateに同じ授業が既に存在するか（追加！）
            same_replacement = Period.objects.filter(
                subject_id=subject_id,
                day_of_week=replacement_weekday,
                period=period.period,
                year=replacement_year,
                semester=replacement_semester
            ).exists()
            if same_replacement:
                messages.error(self.request, '振替先の日付・時間帯にすでに同じ授業が存在します。')
                return self.form_invalid(form)
            
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('attendance:MyPageView')
    
class AttendCheckView(LoginRequiredMixin, ForTeachersMixin, generic.ListView):
    template_name = 'attendance/AttendCheck.html'
    model = Attend
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # user = self.request.user
        pk = self.kwargs.get('pk')
        # print(pk)
        subject = Subject.objects.get(id=pk)
        context['subject'] = subject.subject_name
        periods = Period.objects.filter(subject=subject)
        attends = Attend.objects.filter(period__in=periods).order_by('student__number')
        context['attends'] = attends
        return context
        
def custom_permission_denied_view(request, exception):
    return render(request, '403.html', {'error_message': str(exception)}, status=403)