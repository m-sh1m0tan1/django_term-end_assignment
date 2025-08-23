from django import forms

from .models import *
from .module import JudgePeriod
from datetime import date

class SubjectCreateForm(forms.ModelForm):
    continue_adding = forms.BooleanField(
        label='続けて登録する',
        required=False,
        initial=False,
    )
    
    class Meta:
        model = Subject
        fields = '__all__'
        
class PeriodCreateForm(forms.ModelForm):
    continue_adding = forms.BooleanField(
        label='続けて登録する',
        required=False,
        initial=False,
    )
    
    subject = forms.ModelMultipleChoiceField(
        queryset=Subject.objects.all().order_by('subject_name'),
        label='教科(複数選択可能)',
        widget=forms.SelectMultiple(attrs={'class':'chosen-select'}),
        required=True,
    )
    
    class Meta:
        model = Period
        fields = ['year', 'semester', 'day_of_week', 'period']
        widgets = {
            'semester' : forms.Select(attrs={'class' : 'chosen-select'}),
            'day_of_week' : forms.Select(attrs={'class' : 'chosen-select'}),
            'period' : forms.Select(attrs={'class' : 'chosen-select'}),
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'subject' in self.fields:
            self.fields['subject'].queryset = Subject.objects.order_by('subject_name')
    
class StudentAttendForm(forms.ModelForm):
    class Meta:
        model = Attend
        fields = ('period',)

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        judge = JudgePeriod()
        if judge is not None:
            day_of_week, period_num = judge
            today = date.today()
            # 通常のPeriod
            normal_periods = Period.objects.filter(
                day_of_week=day_of_week+1,
                period=period_num+1,
                year=today.year,
                semester=1 if today.month < 9 else 2
            )
            # 振替授業（今日・この時間帯にReplacementInfoで指定されているもの）
            replacement_infos = ReplacementInfo.objects.filter(
                replacement_date=today,
                replacement_period=period_num+1
            )
            replacement_periods = Period.objects.filter(id__in=replacement_infos.values_list('original_period', flat=True))
            # 通常＋振替を合成
            all_periods = normal_periods | replacement_periods
            self.fields['period'].queryset = all_periods.distinct()
        else:
            self.fields['period'].queryset = Period.objects.none()
            
    def clean(self):
        cleaned_data = super().clean()
        user = self.initial.get('user')
        period = cleaned_data.get('period')
        if user and period:
            # その生徒が同じ曜日・時限・年・学期のPeriodに既に出席していないか
            exists = Attend.objects.filter(
                student=user,
                period__day_of_week=period.day_of_week,
                period__period=period.period,
                period__year=period.year,
                period__semester=period.semester,
            ).exists()
            if exists:
                raise forms.ValidationError('同じ時間帯の授業には既に出席しています。')
        return cleaned_data
    
class PeriodUpdateForm(forms.ModelForm):
    class Meta:
        model = Period
        fields = ['year', 'semester', 'day_of_week', 'period']
        widgets = {
            'semester' : forms.Select(attrs={'class' : 'chosen-select'}),
            'day_of_week' : forms.Select(attrs={'class' : 'chosen-select'}),
            'period' : forms.Select(attrs={'class' : 'chosen-select'}),
            'subject' : forms.Select(attrs={'class' : 'chosen-select', 'disabled' : 'disabled'}),
        }
        
class ReplacementForm(forms.ModelForm):
    class Meta:
        model = ReplacementInfo
        fields = ['original_period', 'reason', 'replacement_period', 'cancel_date', 'replacement_date']
        widgets = {
            'cancel_date' : forms.DateInput(attrs={'type' : 'date'}),
            'replacement_date' : forms.DateInput(attrs={'type' : 'date'})
        }