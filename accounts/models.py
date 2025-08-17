from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator, MinLengthValidator
from django.utils.translation import gettext_lazy as _
# from django.contrib.auth import get_user_model

# User = get_user_model()
# Create your models here.
class User(AbstractUser):
    role_choices = [
        (1, '先生'),
        (2, '生徒'),
    ]
    
    username = models.CharField(
        _('username'),
        max_length=40,
        unique=True,
        help_text=_('必須です。150文字以内で入力してください。日本語も含めた文字、数字、@/./+/-/_ のみ使用できます。'),
        validators=[MinLengthValidator(1)],
        error_messages={
            'username_unique' : _('このユーザー名は既に使用されています。')
        }
    )
    
    role = models.IntegerField(choices=role_choices, null=True, verbose_name='区分')
    number = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(2147483647)], null=True, unique=True, verbose_name='学籍番号', blank=True)
    
    def __str__(self):
        if self.role == 1:
            return f'{self.username}先生'
        elif self.role == 2:
            return f'{self.username}さん'
        return f'部外者 {self.username} {self.email}'