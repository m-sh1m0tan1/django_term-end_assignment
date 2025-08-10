from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from datetime import datetime

# Create your models here.
# 生徒のデータを管理する
# class Student(models.Model):
#     student_name = models.CharField(max_length=16)
#     student_number = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(2147483647)], unique=True)
#     email = models.EmailField(max_length=255, unique=True)
    
#     def __str__(self):
#         return f'{self.student_name} : {self.student_number} : {self.email}'

# 先生のデータを管理する
# class Teacher(models.Model):
#     teacher_name = models.CharField(max_length=16)
#     email = models.EmailField(max_length=255, unique=True)
    
#     def __str__(self):
#         return f'{self.teacher_name} : {self.email}'


# class Teacher(models.Model):
#     teacher_name = models.CharField(max_length=16)
#     email = models.EmailField(max_length=255, unique=True)
    
#     def __str__(self):
#         return self.name
    
    
# 教科のデータを管理する
class Subject(models.Model):
    subject_name = models.CharField(max_length=64, verbose_name='教科名')
    charge_teacher = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, verbose_name='担当教員', limit_choices_to={'role':
        1})
    place = models.IntegerField(validators=[MaxValueValidator(999)], verbose_name='実施する教室', blank=True, null=True)
    
    def __str__(self):
        return f'{self.subject_name} : {self.charge_teacher}'

# 時間割
class Period(models.Model):
    day_of_week_choices = [
        (1, '月曜日'),
        (2, '火曜日'),
        (3, '水曜日'),
        (4, '木曜日'),
        (5, '金曜日'),
    ]
    
    period_choices = [
        (1, '1限目'),
        (2, '2限目'),
        (3, '3限目'),
        (4, '4限目')
    ]
    
    semester_choices = [
        (1, '前期'),
        (2, '後期')
    ]
    day_of_week = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)], choices=day_of_week_choices, verbose_name='曜日')
    period = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(4)], verbose_name='時間帯', choices=period_choices)
    subject = models.ForeignKey(Subject, on_delete=models.PROTECT, verbose_name='教科')
    year = models.PositiveIntegerField(validators=[MinValueValidator(2025)], verbose_name='年(デフォルトは今の年)', default=datetime.now().year, blank=True)
    semester = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(2)], verbose_name='学期', choices=semester_choices)
    class Meta:
        # 全く同じ時間割が入ることを防ぐ
        constraints = [
            models.UniqueConstraint(
                fields=['day_of_week', 'period', 'year', 'semester'],
                name = "period_unique",
            )
        ]
    def __str__(self):
        return f'{self.day_of_week_choices[self.day_of_week - 1][1]}{self.period_choices[self.period - 1][1]} - {self.subject}'

# 出席状況、打刻
class Attend(models.Model):
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, verbose_name='生徒', limit_choices_to={'role': 2})
    period = models.ForeignKey(Period, on_delete=models.PROTECT, verbose_name='授業', limit_choices_to={'year' : datetime.now().year})
    time = models.DateTimeField(auto_now_add=True, verbose_name='打刻時間')
    leave_early = models.BooleanField(default=False, verbose_name='早退フラグ')
    
    class Meta:
        # 同じ生徒が同じ時間割を一日に何回も受けることを防ぐ
        constraints = [
            models.UniqueConstraint(
                fields=["student", "period"],
                name = "student_period_unique",
            )
        ]
    def __str__(self):
        return self.student
    
# 休講・振替用のテーブル
class ReplacementInfo(models.Model):
    original_period = models.ForeignKey(Period, on_delete=models.CASCADE, verbose_name='元の授業')
    replacement_day_of_week = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)], choices=Period.day_of_week_choices, verbose_name='振替曜日')
    replacement_period = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(4)], verbose_name='振替時間帯', choices=Period.day_of_week_choices)
    reason = models.TextField(verbose_name='理由')
    cancel_date = models.DateField(verbose_name='振替日', null=True, blank=True)
    replacement_date = models.DateField(verbose_name='元授業の日付')
    
    class Meta:
    # 振替授業が重複して登録されるのを防ぐ
        constraints = [
            models.UniqueConstraint(
                fields=["original_period", "cancel_date", "replacement_period"],
                name = "cancel_unique",
            )
        ]
    
    def __str__(self):
        return self.original_period