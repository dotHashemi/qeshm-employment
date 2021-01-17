from django.db import models
from django.contrib.auth.models import User

from cities.models import City
from categories.models import Category


class Advertisement(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name="آگهی‌دهنده"
    )
    city = models.ForeignKey(
        City, on_delete=models.PROTECT, verbose_name="شهر"
    )
    category = models.ForeignKey(
        Category, on_delete=models.PROTECT, verbose_name="دسته")
    title = models.CharField(max_length=100, verbose_name="عنوان")
    company = models.CharField(max_length=100, verbose_name="شرکت")
    description = models.TextField(verbose_name="توضیحات")
    isFullTime = models.BooleanField(default=False, verbose_name="تمام وقت")
    isRemote = models.BooleanField(default=False, verbose_name="دورکاری")
    isInternship = models.BooleanField(default=False, verbose_name="کارآموزی")
    isMilitary = models.BooleanField(default=False, verbose_name="امریه")
    salary = models.PositiveIntegerField(
        default=None, null=True, blank=True, verbose_name="حقوق"
    )
    isActive = models.BooleanField(default=True, verbose_name="فعال")
    isVerified = models.BooleanField(default=False, verbose_name="تایید مدیر")
    updated = models.DateTimeField(
        auto_now=True, verbose_name="تاریخ بروزرسانی"
    )
    created = models.DateTimeField(
        auto_now_add=True, verbose_name="تاریخ ایجاد"
    )

    class Meta:
        ordering = ['-id']
        verbose_name = "آگهی"
        verbose_name_plural = "آگهی‌ها"

    def __str__(self):
        return self.title
