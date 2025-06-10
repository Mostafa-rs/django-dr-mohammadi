"""
Accounts models
Mostafa Rasouli
mostafarasooli54@gmail.com
feb 2024
"""

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, AbstractUser, Permission, Group
from django_jalali.db import models as jmodels
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from accounts.manager import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    class Meta:
        verbose_name = 'کاربر'
        verbose_name_plural = 'کاربران'

    GENDER = (
        ('male', 'مرد'),
        ('female', 'زن'),
    )

    MARITAL = (
        ('single', 'مجرد'),
        ('married', 'متاهل'),
        ('unknown', 'نامشخص'),
    )

    phone = models.CharField(max_length=11, unique=True, verbose_name='شماره تماس')
    email = models.EmailField(max_length=150, unique=True, null=True, verbose_name='ایمیل')
    first_name = models.CharField(max_length=255, null=True, verbose_name='نام')
    last_name = models.CharField(max_length=255, null=True, verbose_name='نام خانوادگی')
    gender = models.CharField(max_length=6, choices=GENDER, default='male', verbose_name='جنسیت')
    age = models.PositiveIntegerField(null=True, verbose_name='سن')
    marital = models.CharField(max_length=7, choices=MARITAL, default='unknown', verbose_name='وضعیت تاهل')

    is_admin = models.BooleanField(default=False, verbose_name='مدیر')
    is_active = models.BooleanField(default=True, verbose_name='فعال')
    is_superuser = models.BooleanField(default=False, verbose_name='مدیر سیستم')
    date_joined = jmodels.jDateTimeField(default=timezone.now(), verbose_name='تاریخ عضویت')
    last_login = jmodels.jDateTimeField(blank=True, null=True, verbose_name='اخرین ورود')

    objects = UserManager()

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.phone

    @property
    def is_staff(self):
        return self.is_admin


class UserOtp(models.Model):
    class Meta:
        verbose_name = 'کد تایید'
        verbose_name_plural = 'کد های تایید'

    phone = models.CharField(max_length=11, null=True, blank=True)
    otp = models.CharField(max_length=6, null=True)
    date = models.DateTimeField(null=True)
    expire = models.DateTimeField(null=True)
    used_date = models.DateTimeField(null=True)

    def __str__(self):
        return self.phone
