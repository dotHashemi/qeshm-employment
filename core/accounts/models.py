from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class Account(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, primary_key=True, verbose_name="کاربر"
    )
    type = models.CharField(max_length=10, default=None, verbose_name="نوع")
    created = models.DateTimeField(
        auto_now_add=True, verbose_name="تاریخ ایجاد"
    )

    class Meta:
        verbose_name = "حساب کاربری"
        verbose_name_plural = "حساب‌های کاربری"

    def __str__(self):
        return self.user.username


class Verify(models.Model):
    phone = models.CharField(unique=True, max_length=11, verbose_name="تلفن")
    type = models.CharField(max_length=10, verbose_name="نوع")
    code = models.CharField(max_length=5, default=None, verbose_name="کد")
    isVerified = models.BooleanField(default=False, verbose_name="تایید")
    created = models.DateTimeField(auto_now=True, verbose_name="تاریخ ایجاد")

    class Meta:
        verbose_name = "کد تایید"
        verbose_name_plural = "کدهای تایید"

    def __str__(self):
        return self.phone
