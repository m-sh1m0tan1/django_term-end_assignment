from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.core.validators import MinValueValidator, MaxValueValidator, MinLengthValidator
from django.utils.translation import gettext_lazy as _

class CustomUserManager(BaseUserManager):
    # EmailをログインIDとして扱うためのカスタムユーザーマネージャー
    def create_user(self, email, username, password=None, **extra_fields):
        if not email:
            raise ValueError('Emailは必須です。')
        email = self.normalize_email(email)
        user = self.model(email = email, username = username, **extra_fields)
        user.set_password(password)
        user.save(using=self.db)
        return user
    
    def create_superuser(self, email, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff_True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        
        return self.create_user(email, username, password, **extra_fields)
        
# Create your models here.
class User(AbstractUser):
    role_choices = [
        (1, '先生'),
        (2, '生徒'),
    ]
    
    username = models.CharField(
        _('username'),
        max_length=40,
        help_text=_('表示名として使用します。'),
    )
    
    # emailで認証するのでユニーク制約をつける
    email = models.EmailField(_('email address'), unique=True)
    
    role = models.IntegerField(choices=role_choices, null=True, verbose_name='区分', default=2)
    number = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(2147483647)], null=True, unique=True, verbose_name='学籍番号', blank=True)

    # ログインIDをemailに設定
    USERNAME_FIELD = 'email'
    # createsuperuserコマンドで入力を求められるフィールド
    REQUIRED_FIELDS = ['username']
    
    # 作成したマネージャーをセット
    objects = CustomUserManager()
    
    def __str__(self):
        if self.role == 1:
            return f'{self.username}先生'
        elif self.role == 2:
            return f'{self.username}さん'
        return f'部外者 {self.email}'