from django.db import models


class City(models.Model):
    title = models.CharField(max_length=50, verbose_name="عنوان")

    class Meta:
        verbose_name = "شهر"
        verbose_name_plural = "شهرها"

    def __str__(self):
        return self.title
