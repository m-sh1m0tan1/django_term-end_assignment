from django import forms

from .models import *
from .module import JudgePeriod

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
    class Meta:
        model = Period
        fields = '__all__'
    
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
            self.fields['period'].queryset = Period.objects.filter(day_of_week=day_of_week+1, period=period_num+1)
        else:
            self.fields['period'].queryset = Period.objects.none()