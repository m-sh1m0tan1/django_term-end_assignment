from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.
# 生徒のデータを管理する
class Student(models.Model):
    student_name = models.CharField(max_length=16)
    student_number = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(2147483647)])
    email = models.EmailField(max_length=255)

# 先生のデータを管理する
class Teacher(models.Model):
    teacher_name = models.CharField(max_length=16)
    email = models.EmailField(max_length=255)
    
# 教科のデータを管理する
class Subject(models.Model):
    subject_name = models.CharField(max_length=64)
    charge_teacher_id = models.ForeignKey(Teacher, on_delete=models.PROTECT)
    
# 時間割
class Period(models.Model):
    day_of_week = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    period = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(4)])
    subject = models.ForeignKey(Subject, on_delete=models.PROTECT)
    year = models.PositiveIntegerField(validators=[MinValueValidator(2025)])
    semester = models.IntegerField()

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
    
# 休講用のテーブル
class Cancel(models.Model):
    period = models.ForeignKey(Period)
    reason = models.TextField()
    cancel_datetime = models.DateTimeField()
    change_day_of_week = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    change_period = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(4)])
    