from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import AbstractUser

# Create your models here.
# 生徒のデータを管理する
class Student(models.Model):
    student_name = models.CharField(max_length=16)
    student_number = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(2147483647)], unique=True)
    email = models.EmailField(max_length=255, unique=True)
    
    def __str__(self):
        return f'{self.student_name} : {self.student_number} : {self.email}'

# 先生のデータを管理する
# class Teacher(models.Model):
#     teacher_name = models.CharField(max_length=16)
#     email = models.EmailField(max_length=255, unique=True)
    
#     def __str__(self):
#         return f'{self.teacher_name} : {self.email}'


class Teacher(AbstractUser):
    teacher_name = models.CharField(max_length=16)
    email = models.EmailField(max_length=255, unique=True)
    
    
# 教科のデータを管理する
class Subject(models.Model):
    subject_name = models.CharField(max_length=64)
    charge_teacher = models.ForeignKey(Teacher, on_delete=models.PROTECT)
    place = models.IntegerField()
    
    def __str__(self):
        return f'{self.subject_name} : {self.charge_teacher}'

# 時間割
class Period(models.Model):
    day_of_week = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    period = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(4)])
    subject = models.ForeignKey(Subject, on_delete=models.PROTECT)
    year = models.PositiveIntegerField(validators=[MinValueValidator(2025)])
    semester = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(2)])
    class Meta:
        # 全く同じ時間割が入ることを防ぐ
        constraints = [
            models.UniqueConstraint(
                fields=['day_of_week', 'period', 'year', 'semester'],
                name = "period_unique",
            )
        ]
    def __str__(self):
        return f'{self.day_of_week}.{self.period} : {self.subject}'

# 出席状況、打刻
class Attend(models.Model):
    student = models.ForeignKey(Student, on_delete=models.PROTECT)
    period = models.ForeignKey(Period, on_delete=models.PROTECT)
    time = models.DateTimeField(auto_now_add=True)
    leave_early = models.BooleanField(default=False)
    
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
    original_period = models.ForeignKey(Period, on_delete=models.CASCADE)
    replacement_day_of_week = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    replacement_period = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(4)])
    reason = models.TextField()
    cancel_date = models.DateField()
    replacement_date = models.DateField()
    
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