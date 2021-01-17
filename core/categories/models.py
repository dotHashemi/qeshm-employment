from django.db import models


class Category(models.Model):
    title = models.CharField(max_length=50, verbose_name="عنوان")
    status = models.BooleanField(default=True, verbose_name="وضعیت")
    created = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")

    class Meta:
        verbose_name = "دسته"
        verbose_name_plural = "دسته‌ها"

    def __str__(self):
        return self.title
