from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator
# from django.contrib.auth import get_user_model

# User = get_user_model()
# Create your models here.
class User(AbstractUser):
    role_choices = [
        (1, '先生'),
        (2, '生徒'),
    ]
    role = models.IntegerField(choices=role_choices, null=True, verbose_name='区分')
    number = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(2147483647)], null=True, unique=True, verbose_name='学籍番号', blank=True)
    
    def __str__(self):
        if self.role == 1:
            return f'{self.username}先生'
        elif self.role == 2:
            return f'{self.username}さん'
        return f'部外者 {self.username} {self.email}'