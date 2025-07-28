from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.
class User(AbstractUser):
    role = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(2)], null=True)
    name = models.CharField(max_length=16)
    email = models.EmailField(max_length=255, null=True)
    number = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(2147483647)], null=True)
    
    def __str__(self):
        if self.role == 1:
            return f'先生 {self.name}'
        elif self.role == 2:
            return f'生徒 {self.name}'
        return f'部外者 {self.name} {self.email}'