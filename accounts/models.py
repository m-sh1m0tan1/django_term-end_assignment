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
    role = models.IntegerField(choices=role_choices, null=True)
    # name = models.CharField(max_length=16)
    # email = models.EmailField(max_length=255, null=True)
    number = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(2147483647)], null=True, unique=True)
    
    def __str__(self):
        if self.role == 1:
            return f'先生 {self.username}'
        elif self.role == 2:
            return f'生徒 {self.username}'
        return f'部外者 {self.username} {self.email}'