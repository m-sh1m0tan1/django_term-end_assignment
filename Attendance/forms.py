# attendance/forms.py

from django import forms
from .models import *

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
    
    # def clean(self):
    #     # 1. Djangoの標準的な検証処理を呼び出す前に、まずフォームのデータを取得する
    #     cleaned_data = self.cleaned_data
        
    #     # 2. 必要なフィールドがすべて入力されているか確認する
    #     year = cleaned_data.get('year')
    #     semester = cleaned_data.get('semester')
    #     day_of_week = cleaned_data.get('day_of_week')
    #     period = cleaned_data.get('period')
    #     subject = cleaned_data.get('subject')

    #     # 3. 我々が先回りして、データベースに同じ組み合わせが存在するかチェックする
    #     if all([year, semester, day_of_week, period, subject]):
    #         if Period.objects.filter(
    #             year = year, 
    #             semester = semester,
    #             day_of_week = day_of_week, 
    #             period = period,
    #             subject = subject
    #         ).exists():
    #             # 4.【重要】もし重複があれば、カスタムエラーを発生させて、検証をここで完全に停止する
    #             raise forms.ValidationError(
    #                 'この年度・学期・曜日・時限・科目の組み合わせは既に登録されています。'
    #             )

    #     # 5. 我々のチェックで問題がなければ、Djangoの標準的な検証処理を呼び出して完了させる
    #     return super().clean()